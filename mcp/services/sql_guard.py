from __future__ import annotations

import re

from config import QUERY_LIMIT
from services.catalog import Catalog
from services.db import Database
from services.logger import log_event


FORBIDDEN_KEYWORDS = {
    "alter",
    "analyze",
    "begin",
    "call",
    "commit",
    "copy",
    "create",
    "delete",
    "do",
    "drop",
    "execute",
    "grant",
    "insert",
    "listen",
    "lock",
    "notify",
    "reindex",
    "reset",
    "revoke",
    "rollback",
    "set",
    "show",
    "truncate",
    "update",
    "vacuum",
}

SQL_ALLOWED_KEYWORDS = {
    "where",
    "from",
    "join",
    "left",
    "right",
    "inner",
    "outer",
    "on",
    "as",
    "and",
    "or",
    "not",
    "null",
    "is",
    "in",
    "between",
    "like",
    "ilike",
    "group",
    "by",
    "order",
    "having",
    "limit",
    "offset",
    "distinct",
    "count",
    "sum",
    "avg",
    "min",
    "max",
    "case",
    "when",
    "then",
    "else",
    "end",
    "filter",
    "over",
    "partition",
    "true",
    "false",
}


class SqlValidationError(RuntimeError):
    pass


class SqlGuard:
    def __init__(self, catalog: Catalog, db: Database | None = None):
        self.catalog = catalog
        self.db = db or Database()
        self._columns_cache: dict[tuple[str, str], set[str]] = {}

    def validate(self, sql: str) -> str:
        log_event("sql_guard.validate.start", {"sql": sql})
        cleaned = self._clean(sql)
        lowered = cleaned.lower()

        if not re.match(r"^\s*(select|with)\b", lowered, flags=re.I):
            raise SqlValidationError("Somente SELECT ou WITH sao permitidos.")

        if self._has_multiple_statements(cleaned):
            raise SqlValidationError("Multiplas statements nao sao permitidas.")

        tokens = set(re.findall(r"\b[a-z_][a-z0-9_]*\b", lowered))
        forbidden = sorted(tokens.intersection(FORBIDDEN_KEYWORDS))
        if forbidden:
            raise SqlValidationError(f"Comando/palavra bloqueada no SQL: {', '.join(forbidden)}.")

        refs = self.referenced_tables(cleaned)
        if not refs:
            raise SqlValidationError("A consulta precisa referenciar pelo menos uma tabela com schema.")

        for schema, table in refs:
            if not self.catalog.has_table(schema, table):
                raise SqlValidationError(f"Tabela fora do catalogo/allowlist: {schema}.{table}.")
            table_info = self.catalog.table(schema, table)
            if bool(table_info.get("blocked")):
                raise SqlValidationError(f"Tabela bloqueada no catalogo: {schema}.{table}.")

        blocked_columns = self._blocked_columns(refs)
        used_blocked = [
            column
            for column in blocked_columns
            if re.search(rf"\b{re.escape(column.lower())}\b", lowered)
        ]
        if used_blocked:
            raise SqlValidationError(f"Coluna bloqueada no catalogo: {', '.join(sorted(set(used_blocked)))}.")

        self._validate_real_columns(cleaned, refs)

        log_event("sql_guard.validate.done", {"sql": cleaned, "tables": [f"{schema}.{table}" for schema, table in refs]})
        return cleaned

    def referenced_tables(self, sql: str) -> list[tuple[str, str]]:
        refs = []
        for match in re.finditer(r"\b(?:from|join)\s+([a-z_][a-z0-9_]*)\.([a-z_][a-z0-9_]*)\b", sql, flags=re.I):
            ref = (match.group(1), match.group(2))
            if ref not in refs:
                refs.append(ref)
        return refs

    def table_aliases(self, sql: str) -> set[str]:
        aliases = set()
        pattern = (
            r"\b(?:from|join)\s+"
            r"([a-z_][a-z0-9_]*)\.([a-z_][a-z0-9_]*)"
            r"(?:\s+(?:as\s+)?([a-z_][a-z0-9_]*))?"
        )
        for match in re.finditer(pattern, sql, flags=re.I):
            alias = (match.group(3) or "").lower()
            if alias and alias not in SQL_ALLOWED_KEYWORDS:
                aliases.add(alias)
        return aliases

    def enforce_limit(self, sql: str, limit: int | None = None) -> tuple[str, int]:
        safe_limit = max(1, min(int(limit or QUERY_LIMIT), QUERY_LIMIT))
        return f"select * from ({sql}) as mcp_readonly_query limit {safe_limit}", safe_limit

    def _clean(self, sql: str) -> str:
        value = str(sql or "").strip()
        value = re.sub(r"/\*.*?\*/", " ", value, flags=re.S)
        value = re.sub(r"--.*?$", " ", value, flags=re.M)
        value = value.strip().rstrip(";").strip()
        if not value:
            raise SqlValidationError("SQL vazio.")
        return value

    def _has_multiple_statements(self, sql: str) -> bool:
        return ";" in sql.strip().rstrip(";")

    def _blocked_columns(self, refs: list[tuple[str, str]]) -> set[str]:
        columns = set()
        for schema, table in refs:
            for column in self.catalog.table(schema, table).get("blocked_columns", []):
                columns.add(str(column).lower())
        return columns

    def _validate_real_columns(self, sql: str, refs: list[tuple[str, str]]):
        if len(refs) != 1:
            return
        if re.match(r"^\s*with\b", sql, flags=re.I):
            return

        schema, table = refs[0]
        columns = self._real_columns(schema, table)
        if not columns:
            return

        lowered = self._strip_literals(sql.lower())
        identifiers = set(re.findall(r"\b[a-z_][a-z0-9_]*\b", lowered))
        allowed = set(FORBIDDEN_KEYWORDS).union(SQL_ALLOWED_KEYWORDS)
        allowed.update({schema.lower(), table.lower()})
        allowed.update(self.table_aliases(sql))
        allowed.update({"select", "with", "mcp_readonly_query"})

        unknown_columns = sorted(
            item
            for item in identifiers
            if item not in allowed and item not in columns and self._looks_like_column_reference(lowered, item)
        )
        if unknown_columns:
            raise SqlValidationError(
                f"Coluna inexistente em {schema}.{table}: {', '.join(unknown_columns)}. "
                "Use describe_table/metadata antes de montar a consulta."
            )

    def _real_columns(self, schema: str, table: str) -> set[str]:
        key = (schema, table)
        if key not in self._columns_cache:
            result = self.db.fetch_all(
                """
                select column_name
                from information_schema.columns
                where table_schema = %s
                  and table_name = %s
                """,
                (schema, table),
            )
            self._columns_cache[key] = {str(row["column_name"]).lower() for row in result["rows"]}
        return self._columns_cache[key]

    def _strip_literals(self, sql: str) -> str:
        sql = re.sub(r"'(?:''|[^'])*'", " ", sql)
        sql = re.sub(r'"(?:""|[^"])*"', " ", sql)
        return sql

    def _looks_like_column_reference(self, sql: str, identifier: str) -> bool:
        patterns = [
            rf"\bselect\s+(?:distinct\s+)?{re.escape(identifier)}\b",
            rf"\bwhere\s+{re.escape(identifier)}\b",
            rf"\band\s+{re.escape(identifier)}\b",
            rf"\bor\s+{re.escape(identifier)}\b",
            rf"\bby\s+{re.escape(identifier)}\b",
            rf"\(\s*(?:distinct\s+)?{re.escape(identifier)}\b",
        ]
        return any(re.search(pattern, sql) for pattern in patterns)
