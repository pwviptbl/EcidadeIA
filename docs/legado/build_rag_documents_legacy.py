from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CATALOG_DIR = Path(__file__).resolve().parents[1] / "catalog"
DEFAULT_IA_DIR = Path(__file__).resolve().parents[1] / "knowledge"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "rag" / "catalog_documents.jsonl"


def stable_id(*parts: str) -> str:
    raw = "|".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{parts[0]}:{digest}"


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def infer_markdown_table(path: Path, text: str) -> str | None:
    patterns = [
        r"Tabela Principal:\s*`([^`]+)`",
        r"Tabela principal:\s*`([^`]+)`",
        r"Entidade/Tabela principal\s*\|\s*`([^`]+)`",
        r"Tabela principal\s*\|\s*`([^`]+)`",
        r"\*\*Tabela principal:\*\*\s*`([^`]+)`",
        r"^###\s*`([^`]+)`",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return normalize_markdown_table_name(path, match.group(1))

    if path.parent.name.lower() == "cadastro":
        return f"cadastro.{path.stem.lower()}"
    return None


def normalize_markdown_table_name(path: Path, table_name: str) -> str:
    name = clean(table_name).strip("` ")
    if "." in name:
        return name
    if path.parent.name.lower() == "cadastro":
        return f"cadastro.{name}"
    return name


def markdown_sections(text: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current_title = "Documento"
    current_level = 1
    current_lines: list[str] = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match:
            if current_lines:
                sections.append(
                    {
                        "title": clean(current_title),
                        "level": current_level,
                        "content": "\n".join(current_lines).strip(),
                    }
                )
            current_level = len(match.group(1))
            current_title = match.group(2).strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "title": clean(current_title),
                "level": current_level,
                "content": "\n".join(current_lines).strip(),
            }
        )
    return [section for section in sections if clean(section.get("content"))]


def markdown_sql_blocks(content: str) -> list[str]:
    blocks = []
    for match in re.finditer(r"```(?:sql|postgresql)?\s*\n(.*?)```", content, flags=re.I | re.S):
        sql = match.group(1).strip()
        if sql and re.search(r"\b(select|with)\b", sql, flags=re.I):
            blocks.append(sql)
    return blocks


def markdown_section_kind(title: str, content: str) -> str:
    title_text = title.lower()
    haystack = f"{title} {content}".lower()
    if markdown_sql_blocks(content):
        return "markdown_sql"
    if any(term in title_text for term in ("método", "metodo", "coluna", "auditoria", "crud", "campos obrigatórios", "campos obrigatorios")):
        return "markdown_reference"
    if any(term in haystack for term in ("regra", "cuidado", "risco", "importante", "atenção", "atencao", "não ", "nao ")):
        return "markdown_rule"
    return "markdown_reference"


def markdown_documents(ia_dir: Path) -> list[dict[str, Any]]:
    if not ia_dir.exists():
        return []

    base_dir = ia_dir.parent
    documents: list[dict[str, Any]] = []
    for path in sorted(ia_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(base_dir)
        table_name = infer_markdown_table(path, text)
        domain = table_name.split(".", 1)[0] if table_name and "." in table_name else path.parent.name.lower()

        for index, section in enumerate(markdown_sections(text)):
            title = section["title"]
            content = section["content"]
            kind = markdown_section_kind(title, content)
            document_text = "\n".join(
                item
                for item in [
                    f"Documento Markdown: {relative}",
                    f"Tabela: {table_name}" if table_name else "",
                    f"Secao: {title}",
                    content,
                ]
                if item
            )
            documents.append(
                {
                    "id": stable_id(kind, str(relative), str(index), title),
                    "kind": kind,
                    "text": document_text,
                    "metadata": {
                        "source_file": str(relative),
                        "domain": domain,
                        "schema": domain,
                        "table": table_name,
                        "section": title,
                    },
                }
            )

            for sql_index, sql in enumerate(markdown_sql_blocks(content)):
                documents.append(
                    {
                        "id": stable_id("markdown_sql", str(relative), str(index), str(sql_index), sql[:120]),
                        "kind": "markdown_sql",
                        "text": "\n".join(
                            item
                            for item in [
                                f"SQL documentada em Markdown: {relative}",
                                f"Tabela: {table_name}" if table_name else "",
                                f"Secao: {title}",
                                f"SQL: {clean(sql)}",
                            ]
                            if item
                        ),
                        "metadata": {
                            "source_file": str(relative),
                            "domain": domain,
                            "schema": domain,
                            "table": table_name,
                            "section": title,
                        },
                    }
                )
    return documents


def summarize_type_classification(table: dict[str, Any]) -> str:
    parts: list[str] = []
    mapping = table.get("classificacao_por_tipo") or table.get("type_classification") or {}
    if not isinstance(mapping, dict):
        return ""
    for kind, details in mapping.items():
        if not isinstance(details, dict):
            continue
        chunk = [str(kind)]
        for key in ("coluna_origem", "coluna_chave", "tabela_referencia", "coluna_referencia", "coluna_descricao"):
            value = clean(details.get(key))
            if value:
                chunk.append(f"{key}={value}")
        instruction = clean(details.get("instrucao"))
        if instruction:
            chunk.append(instruction)
        for item in ensure_list(details.get("quando_agrupar")):
            item_text = clean(item)
            if item_text:
                chunk.append(f"agrupar quando {item_text}")
        parts.append("; ".join(chunk))
    return " | ".join(parts)


def table_business_rules(table: dict[str, Any]) -> list[str]:
    return [
        clean(item)
        for item in ensure_list(table.get("logica_negocio") or table.get("business_logic"))
        if clean(item)
    ]


def table_groupings(table: dict[str, Any]) -> list[str]:
    return [
        clean(item)
        for item in ensure_list(table.get("agrupamentos_recomendados") or table.get("recommended_groupings"))
        if clean(item)
    ]


def table_filter_semantics(table: dict[str, Any]) -> dict[str, Any]:
    value = table.get("semantica_filtros") or table.get("filter_semantics") or {}
    return value if isinstance(value, dict) else {}


def table_validated_queries(table: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in ensure_list(table.get("consultas_validadas") or table.get("validated_queries"))
        if isinstance(item, dict)
    ]


def normalize_catalog(raw: dict[str, Any]) -> dict[str, Any]:
    data = dict(raw or {})
    tables = {}
    for table_name, table_info in (data.get("tables") or data.get("tabelas") or {}).items():
        if not isinstance(table_info, dict):
            continue
        columns = {}
        for column_name, column_info in (table_info.get("columns") or table_info.get("colunas") or {}).items():
            if isinstance(column_info, dict):
                columns[column_name] = {
                    **column_info,
                    "description": column_info.get("description") or column_info.get("descricao") or "",
                    "type": column_info.get("type") or column_info.get("tipo"),
                    "semantic_role": column_info.get("semantic_role") or column_info.get("papel") or "",
                    "metric": column_info.get("metric") or column_info.get("metrica") or "",
                    "question_hints": column_info.get("question_hints") or column_info.get("apelidos") or [],
                }
            else:
                columns[column_name] = {"description": column_info}
        foreign_keys = []
        for fk in ensure_list(table_info.get("foreign_keys") or table_info.get("chaves_estrangeiras")):
            if not isinstance(fk, dict):
                continue
            foreign_keys.append(
                {
                    **fk,
                    "references": fk.get("references") or fk.get("referencia"),
                    "referenced_columns": fk.get("referenced_columns") or fk.get("colunas_referenciadas") or [],
                }
            )
        tables[table_name] = {
            **table_info,
            "description": table_info.get("description") or table_info.get("descricao") or "",
            "primary_key": ensure_list(table_info.get("primary_key") or table_info.get("chave_primaria")),
            "entity_key": ensure_list(table_info.get("entity_key") or table_info.get("chave_negocio")),
            "time_key": table_info.get("time_key") or table_info.get("coluna_tempo"),
            "grain": ensure_list(table_info.get("grain") or table_info.get("grao")),
            "default_filters": ensure_list(table_info.get("default_filters") or table_info.get("filtros_padrao")),
            "recommended": bool(table_info.get("recommended") if "recommended" in table_info else table_info.get("recomendada")),
            "columns": columns,
            "foreign_keys": foreign_keys,
        }
    return {
        **data,
        "label": data.get("label") or data.get("rotulo") or data.get("domain"),
        "description": data.get("description") or data.get("descricao") or "",
        "primary_schema": data.get("primary_schema") or data.get("schema_principal"),
        "tables": tables,
        "metrics": {
            metric_name: {
                **metric_info,
                "label": metric_info.get("label") or metric_info.get("rotulo") or "",
                "table": metric_info.get("table") or metric_info.get("tabela"),
                "expression": metric_info.get("expression") or metric_info.get("expressao"),
                "unit": metric_info.get("unit") or metric_info.get("unidade"),
                "description": metric_info.get("description") or metric_info.get("descricao") or "",
                "question_hints": metric_info.get("question_hints") or metric_info.get("apelidos") or [],
                "filter_semantics": metric_info.get("filter_semantics") or metric_info.get("semantica_filtros") or {},
            }
            for metric_name, metric_info in (data.get("metrics") or data.get("metricas") or {}).items()
            if isinstance(metric_info, dict)
        },
        "intents": {
            {
                "comparar_periodos": "compare_periods",
                "contar_registros": "count_records",
            }.get(intent_name, intent_name): {
                **intent_info,
                "description": intent_info.get("description") or intent_info.get("descricao") or "",
                "triggers": intent_info.get("triggers") or intent_info.get("gatilhos") or [],
                "comparison_strategy": intent_info.get("comparison_strategy") or intent_info.get("estrategia_comparacao"),
                "required_dimensions": intent_info.get("required_dimensions") or intent_info.get("dimensoes_obrigatorias") or [],
                "required_entity_key": (
                    intent_info.get("required_entity_key")
                    if "required_entity_key" in intent_info
                    else intent_info.get("exige_chave_negocio")
                ),
                "default_template": intent_info.get("default_template") or intent_info.get("template_padrao"),
                "rules": intent_info.get("rules") or intent_info.get("regras") or [],
                "default_aggregation": intent_info.get("default_aggregation") or intent_info.get("agregacao_padrao"),
            }
            for intent_name, intent_info in (data.get("intents") or data.get("intencoes") or {}).items()
            if isinstance(intent_info, dict)
        },
        "templates": {
            {
                "comparar_periodos_mesma_entidade": "compare_periods_same_entity",
            }.get(template_name, template_name): {
                **template_info,
                "intent": {
                    "comparar_periodos": "compare_periods",
                    "contar_registros": "count_records",
                }.get(template_info.get("intent") or template_info.get("intencao"), template_info.get("intent") or template_info.get("intencao")),
                "strategy": template_info.get("strategy") or template_info.get("estrategia"),
                "requires": template_info.get("requires") or template_info.get("requer") or [],
                "allowed_aggregations": template_info.get("allowed_aggregations") or template_info.get("agregacoes_permitidas") or [],
            }
            for template_name, template_info in (data.get("templates") or data.get("modelos") or {}).items()
            if isinstance(template_info, dict)
        },
        "examples": data.get("examples") or data.get("exemplos") or [],
    }


def load_catalogs(catalog_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    catalogs = []
    for path in sorted(catalog_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            catalogs.append((path, normalize_catalog(json.load(handle))))
    return catalogs


def build_documents(catalogs: list[tuple[Path, dict[str, Any]]]) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for path, catalog in catalogs:
        domain = clean(catalog.get("domain") or path.stem)
        schema = clean(catalog.get("primary_schema") or domain)

        for table_name, table in sorted((catalog.get("tables") or {}).items()):
            documents.append(table_document(path, domain, schema, table_name, table))
            documents.extend(column_documents(path, domain, schema, table_name, table))
            documents.extend(relationship_documents(path, domain, schema, table_name, table))
            documents.extend(business_rule_documents(path, domain, schema, table_name, table))

        for metric_name, metric in sorted((catalog.get("metrics") or {}).items()):
            documents.append(metric_document(path, domain, schema, metric_name, metric))

        for intent_name, intent in sorted((catalog.get("intents") or {}).items()):
            documents.append(intent_document(path, domain, schema, intent_name, intent))

        for index, example in enumerate(catalog.get("examples") or []):
            documents.append(example_document(path, domain, schema, index, example))

    return documents


def table_document(path: Path, domain: str, schema: str, table_name: str, table: dict[str, Any]) -> dict[str, Any]:
    columns = table.get("columns") or {}
    column_names = ", ".join(list(columns.keys())[:60]) if isinstance(columns, dict) else ""
    primary_key = ", ".join(table.get("primary_key") or [])
    entity_key = ", ".join(table.get("entity_key") or [])
    time_key = clean(table.get("time_key"))
    grain = ", ".join(table.get("grain") or [])
    business_logic = " | ".join(table_business_rules(table))
    grouping = " | ".join(table_groupings(table))
    type_classification = summarize_type_classification(table)
    filter_semantics = " | ".join(
        f"{clean(name)}: {clean(expr)}"
        for name, expr in table_filter_semantics(table).items()
        if clean(name) or clean(expr)
    )
    text = "\n".join(
        item
        for item in [
            f"Tabela: {table_name}",
            f"Dominio/schema: {domain}",
            f"Descricao: {clean(table.get('description'))}",
            f"Chave primaria: {primary_key}" if primary_key else "",
            f"Chave da entidade: {entity_key}" if entity_key else "",
            f"Chave temporal: {time_key}" if time_key else "",
            f"Grao analitico: {grain}" if grain else "",
            f"Logica de negocio: {business_logic}" if business_logic else "",
            f"Classificacao por tipo: {type_classification}" if type_classification else "",
            f"Agrupamentos recomendados: {grouping}" if grouping else "",
            f"Semantica de filtros: {filter_semantics}" if filter_semantics else "",
            f"Colunas: {column_names}" if column_names else "",
        ]
        if item
    )
    return {
        "id": stable_id("table", table_name),
        "kind": "table",
        "text": text,
        "metadata": {
            "source_file": path.name,
            "domain": domain,
            "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
            "table": table_name,
            "recommended": bool(table.get("recommended")),
            "primary_key": table.get("primary_key") or [],
            "entity_key": table.get("entity_key") or [],
            "time_key": table.get("time_key"),
        },
    }


def business_rule_documents(
    path: Path,
    domain: str,
    schema: str,
    table_name: str,
    table: dict[str, Any],
) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []

    for index, rule in enumerate(table_business_rules(table)):
        documents.append(
            {
                "id": stable_id("business_rule", table_name, str(index), rule),
                "kind": "business_rule",
                "text": "\n".join(
                    [
                        f"Regra de negocio: {table_name}",
                        f"Tabela: {table_name}",
                        f"Regra: {rule}",
                    ]
                ),
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "rule_type": "business_logic",
                },
            }
        )

    mapping = table.get("classificacao_por_tipo") or table.get("type_classification") or {}
    if isinstance(mapping, dict):
        for kind, details in mapping.items():
            if not isinstance(details, dict):
                continue
            text = "\n".join(
                item
                for item in [
                    f"Classificacao por tipo: {table_name}",
                    f"Tabela: {table_name}",
                    f"Tipo: {clean(kind)}",
                    f"Coluna origem: {clean(details.get('coluna_origem') or details.get('source_column'))}",
                    f"Tabela referencia: {clean(details.get('tabela_referencia') or details.get('reference_table'))}",
                    f"Coluna referencia: {clean(details.get('coluna_referencia') or details.get('reference_column'))}",
                    f"Coluna descricao: {clean(details.get('coluna_descricao') or details.get('description_column'))}",
                    f"Instrucao: {clean(details.get('instrucao') or details.get('instruction'))}",
                    f"Quando agrupar: {' | '.join(clean(item) for item in ensure_list(details.get('quando_agrupar') or details.get('when_to_group')) if clean(item))}",
                ]
                if item
            )
            documents.append(
                {
                    "id": stable_id("classification", table_name, str(kind)),
                    "kind": "classification",
                    "text": text,
                    "metadata": {
                        "source_file": path.name,
                        "domain": domain,
                        "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                        "table": table_name,
                        "classification": kind,
                        "reference_table": details.get("tabela_referencia") or details.get("reference_table"),
                    },
                }
            )

    for name, expression in table_filter_semantics(table).items():
        documents.append(
            {
                "id": stable_id("filter_semantics", table_name, str(name)),
                "kind": "filter_semantics",
                "text": "\n".join(
                    [
                        f"Semantica de filtro: {table_name}",
                        f"Tabela: {table_name}",
                        f"Filtro: {clean(name)}",
                        f"Instrucao: {clean(expression)}",
                    ]
                ),
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "filter": name,
                },
            }
        )

    for index, query in enumerate(table_validated_queries(table)):
        question = clean(query.get("pergunta") or query.get("question"))
        rule = clean(query.get("regra") or query.get("rule"))
        sql = clean(query.get("sql_exemplo") or query.get("sql"))
        documents.append(
            {
                "id": stable_id("validated_query", table_name, str(index), question),
                "kind": "validated_query",
                "text": "\n".join(
                    item
                    for item in [
                        f"Consulta validada: {table_name}",
                        f"Pergunta: {question}",
                        f"Regra: {rule}",
                        f"SQL validada: {sql}",
                    ]
                    if item
                ),
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "question": question,
                },
            }
        )

    for index, grouping in enumerate(table_groupings(table)):
        documents.append(
            {
                "id": stable_id("grouping_rule", table_name, str(index), grouping),
                "kind": "grouping_rule",
                "text": "\n".join(
                    [
                        f"Agrupamento recomendado: {table_name}",
                        f"Tabela: {table_name}",
                        f"Regra: {grouping}",
                    ]
                ),
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "rule_type": "grouping",
                },
            }
        )

    return documents


def column_documents(
    path: Path,
    domain: str,
    schema: str,
    table_name: str,
    table: dict[str, Any],
) -> list[dict[str, Any]]:
    documents = []
    columns = table.get("columns") or {}
    if not isinstance(columns, dict):
        return documents

    for column_name, column in sorted(columns.items()):
        column = column if isinstance(column, dict) else {"description": column}
        semantic_role = clean(column.get("semantic_role"))
        metric = clean(column.get("metric"))
        text = "\n".join(
            item
            for item in [
                f"Coluna: {table_name}.{column_name}",
                f"Tabela: {table_name}",
                f"Dominio/schema: {domain}",
                f"Tipo: {clean(column.get('type'))}",
                f"Descricao: {clean(column.get('description'))}",
                f"Papel semantico: {semantic_role}" if semantic_role else "",
                f"Metrica: {metric}" if metric else "",
            ]
            if item
        )
        documents.append(
            {
                "id": stable_id("column", table_name, column_name),
                "kind": "column",
                "text": text,
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "column": column_name,
                    "type": column.get("type"),
                    "semantic_role": column.get("semantic_role") or "",
                    "metric": column.get("metric") or "",
                },
            }
        )
    return documents


def relationship_documents(
    path: Path,
    domain: str,
    schema: str,
    table_name: str,
    table: dict[str, Any],
) -> list[dict[str, Any]]:
    documents = []
    for index, fk in enumerate(table.get("foreign_keys") or []):
        columns = ", ".join(fk.get("columns") or [])
        referenced_columns = ", ".join(fk.get("referenced_columns") or [])
        target = clean(fk.get("references"))
        text = "\n".join(
            item
            for item in [
                f"Relacionamento: {table_name} -> {target}",
                f"Colunas origem: {columns}" if columns else "",
                f"Colunas destino: {referenced_columns}" if referenced_columns else "",
                f"Constraint: {clean(fk.get('constraint'))}",
            ]
            if item
        )
        documents.append(
            {
                "id": stable_id("relationship", table_name, str(index), target),
                "kind": "relationship",
                "text": text,
                "metadata": {
                    "source_file": path.name,
                    "domain": domain,
                    "schema": table_name.split(".", 1)[0] if "." in table_name else schema,
                    "table": table_name,
                    "references": target,
                    "columns": fk.get("columns") or [],
                    "referenced_columns": fk.get("referenced_columns") or [],
                },
            }
        )
    return documents


def metric_document(path: Path, domain: str, schema: str, metric_name: str, metric: dict[str, Any]) -> dict[str, Any]:
    text = "\n".join(
        item
        for item in [
            f"Metrica: {metric_name}",
            f"Rotulo: {clean(metric.get('label'))}",
            f"Tabela: {clean(metric.get('table'))}",
            f"Expressao: {clean(metric.get('expression'))}",
            f"Unidade: {clean(metric.get('unit'))}",
            f"Descricao: {clean(metric.get('description'))}",
        ]
        if item
    )
    return {
        "id": stable_id("metric", domain, metric_name),
        "kind": "metric",
        "text": text,
        "metadata": {
            "source_file": path.name,
            "domain": domain,
            "schema": schema,
            "metric": metric_name,
            "table": metric.get("table"),
            "expression": metric.get("expression"),
            "unit": metric.get("unit"),
            "explain_variation": bool(metric.get("explain_variation")),
        },
    }


def intent_document(path: Path, domain: str, schema: str, intent_name: str, intent: dict[str, Any]) -> dict[str, Any]:
    triggers = ", ".join(intent.get("triggers") or [])
    rules = " ".join(intent.get("rules") or [])
    text = "\n".join(
        item
        for item in [
            f"Intencao analitica: {intent_name}",
            f"Descricao: {clean(intent.get('description'))}",
            f"Gatilhos: {triggers}" if triggers else "",
            f"Estrategia: {clean(intent.get('comparison_strategy'))}",
            f"Template padrao: {clean(intent.get('default_template'))}",
            f"Regras: {clean(rules)}" if rules else "",
        ]
        if item
    )
    return {
        "id": stable_id("intent", domain, intent_name),
        "kind": "intent",
        "text": text,
        "metadata": {
            "source_file": path.name,
            "domain": domain,
            "schema": schema,
            "intent": intent_name,
            "default_template": intent.get("default_template"),
        },
    }


def example_document(path: Path, domain: str, schema: str, index: int, example: dict[str, Any]) -> dict[str, Any]:
    question = clean(example.get("question") or example.get("pergunta"))
    sql = clean(example.get("sql"))
    answer = clean(example.get("answer") or example.get("resposta"))
    text = "\n".join(
        item
        for item in [
            f"Exemplo de pergunta: {question}" if question else "",
            f"SQL exemplo: {sql}" if sql else "",
            f"Resposta exemplo: {answer}" if answer else "",
        ]
        if item
    )
    return {
        "id": stable_id("example", domain, str(index), question),
        "kind": "example",
        "text": text,
        "metadata": {
            "source_file": path.name,
            "domain": domain,
            "schema": schema,
            "question": question,
        },
    }


def write_jsonl(path: Path, documents: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for document in documents:
            handle.write(json.dumps(document, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Converte catalogos JSON em documentos JSONL para RAG.")
    parser.add_argument("--catalog-dir", type=Path, default=DEFAULT_CATALOG_DIR)
    parser.add_argument("--ia-dir", type=Path, default=DEFAULT_IA_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    catalogs = load_catalogs(args.catalog_dir)
    documents = build_documents(catalogs)
    documents.extend(markdown_documents(args.ia_dir))
    write_jsonl(args.output, documents)
    counts: dict[str, int] = {}
    for document in documents:
        counts[document["kind"]] = counts.get(document["kind"], 0) + 1
    print(
        json.dumps(
            {
                "catalog_dir": str(args.catalog_dir),
                "ia_dir": str(args.ia_dir),
                "output": str(args.output),
                "documents": len(documents),
                "counts": counts,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
