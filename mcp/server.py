from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from config import (
    MCP_ALLOWED_HOSTS,
    MCP_ALLOWED_ORIGINS,
    MCP_DISABLE_DNS_REBINDING_PROTECTION,
    MCP_HOST,
    MCP_PORT,
    MCP_TRANSPORT,
)
from services.audit import write_audit
from services.catalog import Catalog
from services.db import Database
from services.logger import log_event
from services.rag import RagIndex
from services.sql_guard import SqlGuard


transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=not MCP_DISABLE_DNS_REBINDING_PROTECTION,
    allowed_hosts=MCP_ALLOWED_HOSTS,
    allowed_origins=MCP_ALLOWED_ORIGINS,
)

mcp = FastMCP(
    "ecidade-readonly",
    host=MCP_HOST,
    port=MCP_PORT,
    transport_security=transport_security,
)
catalog = Catalog()
rag = RagIndex()
db = Database()
guard = SqlGuard(catalog, db)


def _split_table(full_name: str) -> tuple[str, str]:
    parts = str(full_name or "").strip().split(".", 1)
    if len(parts) != 2:
        raise ValueError("Informe a tabela no formato schema.tabela.")
    return parts[0], parts[1]


@mcp.tool()
def ecidade_health() -> dict[str, Any]:
    """Verifica se o MCP consegue conectar no banco PostgreSQL read-only."""
    log_event("tool.health.start")
    payload = db.health()
    write_audit("health", payload)
    log_event("tool.health.done", payload)
    return {"ok": True, "database": payload}


@mcp.tool()
def ecidade_catalog_index() -> dict[str, Any]:
    """Retorna o catalogo consolidado de dominios, tabelas e campos permitidos."""
    payload = catalog.index()
    log_event("tool.catalog_index", {"tables": len(payload.get("tables", {}))})
    return payload


@mcp.tool()
def ecidade_catalog_search(text: str, limit: int = 20) -> dict[str, Any]:
    """Busca tabelas/campos no catalogo por texto de negocio ou nome tecnico."""
    results = rag.search_tables(text, catalog, limit) if rag.loaded else []
    source = "rag" if results else "catalog"
    if not results:
        results = catalog.search(text, limit)
    log_event(
        "tool.catalog_search",
        {
            "text": text,
            "limit": limit,
            "source": source,
            "results": [item.get("table") for item in results],
        },
    )
    return {"results": results}


@mcp.tool()
def ecidade_catalog_rag_search(text: str, limit: int = 20, kinds: list[str] | None = None) -> dict[str, Any]:
    """Busca documentos RAG do catalogo por texto de negocio ou nome tecnico."""
    results = rag.search(text, limit, kinds=kinds)
    log_event(
        "tool.catalog_rag_search",
        {
            "text": text,
            "limit": limit,
            "kinds": kinds or [],
            "results": len(results),
        },
    )
    return {"results": results, "loaded": rag.loaded}


@mcp.tool()
def ecidade_list_schemas() -> dict[str, Any]:
    """Lista schemas autorizados pelo catalogo/allowlist do MCP."""
    return {"schemas": catalog.schemas()}


@mcp.tool()
def ecidade_list_tables(schema: str) -> dict[str, Any]:
    """Lista tabelas catalogadas para um schema autorizado."""
    schema = str(schema or "").strip()
    tables = [
        {"name": name, "description": catalog.data["tables"][name].get("description")}
        for name in catalog.table_names()
        if name.startswith(f"{schema}.")
    ]
    return {"schema": schema, "tables": tables}


@mcp.tool()
def ecidade_describe_table(schema: str, table: str) -> dict[str, Any]:
    """Descreve uma tabela catalogada e complementa com metadados reais do banco."""
    log_event("tool.describe_table.start", {"schema": schema, "table": table})
    schema = str(schema or "").strip()
    table = str(table or "").strip()
    if not catalog.has_table(schema, table):
        raise ValueError(f"Tabela fora do catalogo/allowlist: {schema}.{table}")

    metadata = db.fetch_all(
        """
        select
            column_name,
            data_type,
            is_nullable,
            character_maximum_length,
            numeric_precision,
            numeric_scale
        from information_schema.columns
        where table_schema = %s
          and table_name = %s
        order by ordinal_position
        """,
        (schema, table),
    )
    payload = {
        "table": f"{schema}.{table}",
        "catalog": catalog.table(schema, table),
        "columns": metadata["rows"],
    }
    log_event("tool.describe_table.done", {"table": payload["table"], "columns": len(payload["columns"])})
    return payload


@mcp.tool()
def ecidade_get_relationships(tables: list[str] | None = None) -> dict[str, Any]:
    """Retorna relacionamentos declarados no catalogo para as tabelas informadas."""
    requested = set(tables or catalog.table_names())
    relationships = []
    for full_name in catalog.table_names():
        if full_name not in requested:
            continue
        info = catalog.data["tables"].get(full_name, {})
        for fk in info.get("foreign_keys", []):
            relationships.append(
                {
                    "kind": "foreign_key",
                    "source_table": full_name,
                    "source_column": fk.get("column"),
                    "target": fk.get("references"),
                }
            )
        for rel in info.get("semantic_relationships", []):
            if not isinstance(rel, dict):
                continue
            relationships.append(
                {
                    "kind": "semantic_path",
                    "source_table": full_name,
                    "target_table": rel.get("target"),
                    "hops": rel.get("hops"),
                    "path": rel.get("path") or [],
                    "join_chain": rel.get("join_chain") or [],
                }
            )
    log_event("tool.relationships", {"tables": tables or [], "relationships": len(relationships)})
    return {"relationships": relationships}


@mcp.tool()
def ecidade_readonly_query(sql: str, limit: int = 1000, statement_timeout_ms: int | None = None) -> dict[str, Any]:
    """Executa uma consulta SELECT/WITH read-only em tabelas permitidas pelo catalogo."""
    log_event("tool.query.start", {"sql": sql, "limit": limit, "statement_timeout_ms": statement_timeout_ms})
    validated_sql = guard.validate(sql)
    limited_sql, safe_limit = guard.enforce_limit(validated_sql, limit)
    payload = db.fetch_all(limited_sql, statement_timeout_ms=statement_timeout_ms)
    result = {
        "sql": validated_sql,
        "limit": safe_limit,
        "row_count": payload["row_count"],
        "duration_ms": payload["duration_ms"],
        "rows": payload["rows"],
    }
    write_audit(
        "readonly_query",
        {
            "sql": validated_sql,
            "limit": safe_limit,
            "statement_timeout_ms": statement_timeout_ms,
            "row_count": payload["row_count"],
            "duration_ms": payload["duration_ms"],
            "tables": [f"{schema}.{table}" for schema, table in guard.referenced_tables(validated_sql)],
        },
    )
    log_event(
        "tool.query.done",
        {
            "sql": validated_sql,
            "limit": safe_limit,
            "statement_timeout_ms": statement_timeout_ms,
            "row_count": payload["row_count"],
            "duration_ms": payload["duration_ms"],
        },
    )
    return result


if __name__ == "__main__":
    mcp.run(transport=MCP_TRANSPORT)

@mcp.tool()
def ecidade_validate_sql_explain(sql: str) -> dict[str, Any]:
    """Executa um EXPLAIN na query para validar estaticamente se a sintaxe e as tabelas/colunas estao corretas antes da execucao real."""
    log_event("tool.explain.start", {"sql": sql})
    validated_sql = guard.validate(sql)
    explain_sql = f"EXPLAIN {validated_sql}"
    try:
        payload = db.fetch_all(explain_sql)
        result = {
            "valid": True,
            "explain_plan": payload["rows"]
        }
    except Exception as e:
        result = {
            "valid": False,
            "error": str(e)
        }
    log_event("tool.explain.done", {"sql": validated_sql, "valid": result["valid"]})
    return result
