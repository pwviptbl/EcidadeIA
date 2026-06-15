import json
import re
from pathlib import Path

from config import CATALOG_DIR


SEARCH_STOPWORDS = {
    "a",
    "as",
    "o",
    "os",
    "de",
    "do",
    "da",
    "dos",
    "das",
    "e",
    "em",
    "no",
    "na",
    "nos",
    "nas",
    "tem",
    "temos",
    "quantos",
    "quantas",
    "quanto",
    "quanta",
    "total",
    "contar",
    "existe",
    "existem",
    "compare",
    "comparar",
    "explique",
    "explicar",
    "principais",
    "principal",
    "fatores",
    "fator",
    "aumento",
    "reducao",
    "redução",
    "variacao",
    "variação",
    "evolucao",
    "evolução",
}


class Catalog:
    def __init__(self, path: Path | None = None, mcp_client=None):
        self.path = path
        self.mcp_client = mcp_client
        self.data = self._load()

    def _load(self) -> dict:
        if self.mcp_client:
            return self.mcp_client.catalog_index()

        if self.path:
            with self.path.open("r", encoding="utf-8") as handle:
                return json.load(handle)

        domains = []
        tables = {}
        examples = []
        primary_schemas = []
        intents = {}
        metrics = {}
        templates = {}

        for path in sorted(CATALOG_DIR.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            domain_tables = {
                table_name: self._normalize_table_info(table_info)
                for table_name, table_info in (data.get("tables") or data.get("tabelas") or {}).items()
                if isinstance(table_info, dict)
            }

            domains.append(
                {
                    "domain": data.get("domain") or path.stem,
                    "label": data.get("label") or data.get("rotulo") or path.stem,
                    "description": data.get("description") or data.get("descricao") or "",
                    "primary_schema": data.get("primary_schema") or data.get("schema_principal"),
                }
            )
            primary_schema = data.get("primary_schema") or data.get("schema_principal")
            if primary_schema and primary_schema not in primary_schemas:
                primary_schemas.append(primary_schema)

            tables.update(domain_tables)
            examples.extend(data.get("examples") or data.get("exemplos") or [])
            intents.update(data.get("intents") or data.get("intencoes") or {})
            metrics.update(data.get("metrics") or data.get("metricas") or {})
            templates.update(data.get("templates") or data.get("modelos") or {})

        return {
            "domain": "ecidade",
            "label": "e-Cidade",
            "description": "Catalogo consolidado de dominios do e-Cidade.",
            "primary_schema": primary_schemas[0] if len(primary_schemas) == 1 else None,
            "domains": domains,
            "intents": intents,
            "metrics": metrics,
            "templates": templates,
            "tables": tables,
            "examples": examples,
        }

    def _normalize_table_info(self, info: dict) -> dict:
        columns = info.get("columns") or info.get("colunas") or {}
        foreign_keys = []
        for fk in info.get("foreign_keys") or info.get("chaves_estrangeiras") or []:
            if not isinstance(fk, dict):
                continue
            foreign_keys.append(
                {
                    **fk,
                    "references": fk.get("references") or fk.get("referencia"),
                    "referenced_columns": fk.get("referenced_columns") or fk.get("colunas_referenciadas") or [],
                }
            )
        return {
            **info,
            "description": info.get("description") or info.get("descricao") or "",
            "columns": columns,
            "primary_key": info.get("primary_key") or info.get("chave_primaria") or [],
            "grain": info.get("grain") or info.get("grao") or [],
            "entity_key": info.get("entity_key") or info.get("chave_negocio") or [],
            "time_key": info.get("time_key") or info.get("coluna_tempo"),
            "default_filters": info.get("default_filters") or info.get("filtros_padrao") or [],
            "foreign_keys": foreign_keys,
            "business_logic": info.get("business_logic") or info.get("logica_negocio") or [],
            "filter_semantics": info.get("filter_semantics") or info.get("semantica_filtros") or {},
            "type_classification": info.get("type_classification") or info.get("classificacao_por_tipo") or {},
            "recommended_groupings": info.get("recommended_groupings") or info.get("agrupamentos_recomendados") or [],
            "validated_queries": info.get("validated_queries") or info.get("consultas_validadas") or [],
            "business_notes": info.get("business_notes") or info.get("observacoes_negocio") or [],
            "recommended": bool(info.get("recommended") if "recommended" in info else info.get("recomendada")),
        }

    def domain_summary(self) -> str:
        tables = self.data.get("tables", {})
        lines = [
            f"Dominio: {self.data.get('label')}",
            self.data.get("description", ""),
            "",
            "Tabelas iniciais:",
        ]
        for name, info in tables.items():
            marker = "principal" if info.get("recommended") else "apoio"
            lines.append(f"- {name} ({marker}): {info.get('description', 'sem descricao')}")
        return "\n".join(lines).strip()

    def table_names(self) -> list[str]:
        return list(self.data.get("tables", {}).keys())

    def table(self, full_name: str) -> dict:
        return self.data.get("tables", {}).get(full_name, {})

    def search(self, text: str, limit: int = 8) -> list[dict]:
        if self.mcp_client:
            return self.mcp_client.search_docs(text).get("results", [])[:limit]

        terms = self._search_terms(text)
        results = []
        for name, info in self.data.get("tables", {}).items():
            score = self._score_table(name, info, terms)
            if not terms or score:
                results.append(
                    {
                        "table": name,
                        "description": info.get("description"),
                        "columns": info.get("columns", {}),
                        "grain": info.get("grain", []),
                        "entity_key": info.get("entity_key", []),
                        "time_key": info.get("time_key"),
                        "recommended": bool(info.get("recommended")),
                        "score": score,
                    }
                )
        results.sort(key=lambda item: (item["score"], item["recommended"]), reverse=True)
        return results[:limit]

    def _search_terms(self, text: str) -> list[str]:
        terms = []
        for term in re.findall(r"[a-z0-9_]+", str(text or "").lower()):
            if term in SEARCH_STOPWORDS or term.isdigit() or len(term) < 2:
                continue
            terms.append(term)
        return terms

    def _score_table(self, full_name: str, info: dict, terms: list[str]) -> int:
        schema, _, table_name = full_name.partition(".")
        table_tokens = set(self._tokens(table_name))
        description_tokens = set(self._tokens(info.get("description", "")))
        columns = info.get("known_columns") or info.get("columns", {})
        column_names = set(columns.keys()) if isinstance(columns, dict) else set()
        column_tokens = set()
        for column_name, column_info in columns.items() if isinstance(columns, dict) else []:
            column_tokens.update(self._tokens(column_name))
            if isinstance(column_info, dict):
                column_tokens.update(self._tokens(column_info.get("description", "")))
            else:
                column_tokens.update(self._tokens(column_info))

        score = 0
        for term in terms:
            normalized = self._singular(term)
            if term == table_name or normalized == self._singular(table_name):
                score += 80
            elif table_name.startswith(term) or term.startswith(table_name):
                score += 40

            if normalized in {self._singular(token) for token in table_tokens}:
                score += 30
            if normalized in {self._singular(token) for token in description_tokens}:
                score += 12
            if term in column_names:
                score += 8
            if normalized in {self._singular(token) for token in column_tokens}:
                score += 4
            if term == schema:
                score += 2
        return score

    def _tokens(self, value) -> list[str]:
        return re.findall(r"[a-z0-9_]+", str(value or "").lower())

    def _singular(self, value: str) -> str:
        if len(value) > 3 and value.endswith("s"):
            return value[:-1]
        return value

    def schemas(self) -> list[str]:
        schemas = set()
        if self.data.get("primary_schema"):
            schemas.add(str(self.data["primary_schema"]))

        for domain in self.data.get("domains", []):
            if domain.get("primary_schema"):
                schemas.add(str(domain["primary_schema"]))

        for table_name in self.table_names():
            if "." in table_name:
                schemas.add(table_name.split(".", 1)[0])

        return sorted(schemas)

    def default_schema(self) -> str | None:
        schemas = self.schemas()
        if len(schemas) == 1:
            return schemas[0]
        return self.data.get("primary_schema")

    def index(self) -> dict:
        return self._index(compact=False)

    def compact_index(self) -> dict:
        return self._index(compact=True)

    def _index(self, compact: bool) -> dict:
        tables = {}
        for name, info in self.data.get("tables", {}).items():
            columns = info.get("known_columns") or info.get("columns", {})
            table = {
                "description": info.get("description"),
                "primary_key": info.get("primary_key", []),
                "grain": info.get("grain", []),
                "entity_key": info.get("entity_key", []),
                "time_key": info.get("time_key"),
                "default_filters": info.get("default_filters", []),
                "recommended": bool(info.get("recommended")),
                "business_logic": info.get("business_logic", []),
                "filter_semantics": info.get("filter_semantics", {}),
                "type_classification": info.get("type_classification", {}),
                "recommended_groupings": info.get("recommended_groupings", []),
                "validated_queries": info.get("validated_queries", []),
                "business_notes": info.get("business_notes", []),
            }
            if compact:
                table["columns"] = list(columns.keys())[:20]
            else:
                table["known_columns"] = columns
                table["blocked_columns"] = info.get("blocked_columns", [])
            tables[name] = table

        return {
            "domain": self.data.get("domain"),
            "label": self.data.get("label"),
            "description": self.data.get("description"),
            "primary_schema": self.data.get("primary_schema"),
            "domains": self.data.get("domains", []),
            "intents": self.data.get("intents", {}),
            "metrics": self.data.get("metrics", {}),
            "templates": self.data.get("templates", {}),
            "schemas": self.schemas(),
            "tables": tables,
            "examples": self.data.get("examples", []),
        }
