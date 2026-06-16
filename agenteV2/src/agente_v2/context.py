from __future__ import annotations

import re
from typing import Any

from agente_v2.config import CATALOG_SEARCH_LIMIT, RAG_LIMIT
from agente_v2.infrastructure.logger import log_event
from agente_v2.infrastructure.mcp import McpClient


RAG_KINDS = [
    "business_concept",
    "relationship_recipe",
    "business_filter",
    "table_role",
    "counting_rule",
    "markdown_rule",
    "markdown_reference",
    "classification",
    "filter_semantics",
    "grouping_rule",
]


def build_context(question: str, mcp: McpClient) -> dict[str, Any]:
    catalog_results = (mcp.catalog_search(question, CATALOG_SEARCH_LIMIT).get("results") or [])[:CATALOG_SEARCH_LIMIT]
    rag_results = (mcp.rag_search(question, RAG_LIMIT, RAG_KINDS).get("results") or [])[:RAG_LIMIT]
    tables = _selected_tables(catalog_results, rag_results)
    described = {}
    for table in tables[:14]:
        try:
            described[table] = mcp.describe_table(table)
        except Exception as exc:
            described[table] = {"error": str(exc)}
    relationships = {}
    if tables:
        try:
            relationships = mcp.relationships(tables[:14])
        except Exception as exc:
            relationships = {"error": str(exc), "relationships": []}

    context = {
        "catalog_results": catalog_results,
        "rag_results": rag_results,
        "tables": tables,
        "described_tables": described,
        "relationships": relationships.get("relationships") or [],
    }
    log_event(
        "context.built",
        {
            "tables": tables,
            "catalog_results": len(catalog_results),
            "rag_results": len(rag_results),
            "relationships": len(context["relationships"]),
        },
    )
    return context


def _selected_tables(catalog_results: list[dict], rag_results: list[dict]) -> list[str]:
    tables: list[str] = []
    for item in catalog_results:
        table = str(item.get("table") or "").strip()
        if table and table not in tables:
            tables.append(table)
    for item in rag_results:
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        table = str(item.get("table") or metadata.get("table") or "").strip()
        if table and "." in table and table not in tables:
            tables.append(table)
        text = str(item.get("text") or "")
        for referenced_table in re.findall(r"\bcadastro\.[a-zA-Z_][a-zA-Z0-9_]*\b", text):
            if referenced_table not in tables:
                tables.append(referenced_table)
    return tables


def compact_context(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "tables": context.get("tables", [])[:12],
        "catalog_candidates": [
            {
                "table": item.get("table"),
                "description": item.get("description"),
                "columns": item.get("columns"),
                "score": item.get("score"),
                "rag_evidence": _compact_evidence(item.get("rag_evidence") or []),
            }
            for item in (context.get("catalog_results") or [])[:10]
        ],
        "business_evidence": [
            {
                "kind": item.get("kind"),
                "table": (item.get("metadata") or {}).get("table") if isinstance(item.get("metadata"), dict) else item.get("table"),
                "text": str(item.get("text") or "")[:1600],
            }
            for item in (context.get("rag_results") or [])[:12]
        ],
        "relationships": (context.get("relationships") or [])[:20],
        "described_tables": {
            table: _compact_describe(payload)
            for table, payload in (context.get("described_tables") or {}).items()
        },
    }


def _compact_evidence(items: list[dict]) -> list[dict]:
    result = []
    for item in items[:4]:
        if not isinstance(item, dict):
            continue
        result.append({"kind": item.get("kind"), "text": str(item.get("text") or "")[:500]})
    return result


def _compact_describe(payload: dict) -> dict:
    catalog = payload.get("catalog") if isinstance(payload.get("catalog"), dict) else {}
    columns = payload.get("columns") or catalog.get("columns") or catalog.get("colunas") or []
    if isinstance(columns, dict):
        column_names = list(columns.keys())
    elif isinstance(columns, list):
        column_names = [str(item.get("name") or item.get("column") or item) for item in columns[:80]]
    else:
        column_names = []
    return {
        "table": payload.get("table") or catalog.get("table"),
        "description": catalog.get("description") or catalog.get("descricao"),
        "primary_key": catalog.get("primary_key") or catalog.get("chave_primaria"),
        "entity_key": catalog.get("entity_key") or catalog.get("chave_negocio"),
        "time_key": catalog.get("time_key") or catalog.get("coluna_tempo"),
        "columns": column_names[:80],
        "error": payload.get("error"),
    }
