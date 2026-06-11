from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
MCP_DIR = ROOT_DIR / "mcp"
sys.path.insert(0, str(MCP_DIR))

from config import CATALOG_DIR, KNOWLEDGE_DIR, RAG_DOCUMENTS_PATH  # noqa: E402


IA_DIR = KNOWLEDGE_DIR / "rag"
OUTPUT_PATH = RAG_DOCUMENTS_PATH


def doc_id(kind: str, *parts: str) -> str:
    raw = "|".join([kind, *parts]).encode("utf-8")
    return f"{kind}:{hashlib.sha1(raw).hexdigest()[:12]}"


def compact_text(value: object) -> str:
    return " ".join(str(value or "").split())


def ensure_list(value: object) -> list:
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
    name = compact_text(table_name).strip("` ")
    if "." in name:
        return name
    if path.parent.name.lower() == "cadastro":
        return f"cadastro.{name}"
    return name


def markdown_sections(text: str) -> list[dict]:
    sections: list[dict] = []
    current_title = "Documento"
    current_level = 1
    current_lines: list[str] = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match:
            if current_lines:
                sections.append(
                    {
                        "title": compact_text(current_title),
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
                "title": compact_text(current_title),
                "level": current_level,
                "content": "\n".join(current_lines).strip(),
            }
        )
    return [section for section in sections if compact_text(section.get("content"))]


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


def build_markdown_docs() -> list[dict]:
    if not IA_DIR.exists():
        return []

    docs: list[dict] = []
    for path in sorted(IA_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT_DIR)
        table_name = infer_markdown_table(path, text)
        domain = table_name.split(".", 1)[0] if table_name and "." in table_name else path.parent.name.lower()

        for index, section in enumerate(markdown_sections(text)):
            title = section["title"]
            content = section["content"]
            kind = markdown_section_kind(title, content)
            section_text = "\n".join(
                item
                for item in [
                    f"Documento Markdown: {relative}",
                    f"Tabela: {table_name}" if table_name else "",
                    f"Secao: {title}",
                    content,
                ]
                if item
            )
            docs.append(
                {
                    "id": doc_id(kind, str(relative), str(index), title),
                    "kind": kind,
                    "metadata": {
                        "domain": domain,
                        "schema": domain,
                        "source_file": str(relative),
                        "table": table_name,
                        "section": title,
                    },
                    "text": section_text,
                }
            )

            for sql_index, sql in enumerate(markdown_sql_blocks(content)):
                docs.append(
                    {
                        "id": doc_id("markdown_sql", str(relative), str(index), str(sql_index), sql[:120]),
                        "kind": "markdown_sql",
                        "metadata": {
                            "domain": domain,
                            "schema": domain,
                            "source_file": str(relative),
                            "table": table_name,
                            "section": title,
                        },
                        "text": "\n".join(
                            item
                            for item in [
                                f"SQL documentada em Markdown: {relative}",
                                f"Tabela: {table_name}" if table_name else "",
                                f"Secao: {title}",
                                f"SQL: {compact_text(sql)}",
                            ]
                            if item
                        ),
                    }
                )
    return docs


def summarize_type_classification(table_info: dict) -> str:
    parts: list[str] = []
    mapping = table_info.get("classificacao_por_tipo") or table_info.get("type_classification") or {}
    if not isinstance(mapping, dict):
        return ""
    for kind, details in mapping.items():
        if not isinstance(details, dict):
            continue
        chunk = [compact_text(kind)]
        for key in ("coluna_origem", "coluna_chave", "tabela_referencia", "coluna_referencia", "coluna_descricao"):
            value = compact_text(details.get(key))
            if value:
                chunk.append(f"{key}={value}")
        instruction = compact_text(details.get("instrucao"))
        if instruction:
            chunk.append(instruction)
        for item in ensure_list(details.get("quando_agrupar")):
            item_text = compact_text(item)
            if item_text:
                chunk.append(f"agrupar quando {item_text}")
        parts.append("; ".join(chunk))
    return " | ".join(parts)


def table_business_rules(table_info: dict) -> list[str]:
    return [
        compact_text(item)
        for item in ensure_list(table_info.get("logica_negocio") or table_info.get("business_logic"))
        if compact_text(item)
    ]


def table_groupings(table_info: dict) -> list[str]:
    return [
        compact_text(item)
        for item in ensure_list(table_info.get("agrupamentos_recomendados") or table_info.get("recommended_groupings"))
        if compact_text(item)
    ]


def table_filter_semantics(table_info: dict) -> dict:
    value = table_info.get("semantica_filtros") or table_info.get("filter_semantics") or {}
    return value if isinstance(value, dict) else {}


def table_validated_queries(table_info: dict) -> list[dict]:
    return [
        item
        for item in ensure_list(table_info.get("consultas_validadas") or table_info.get("validated_queries"))
        if isinstance(item, dict)
    ]


def normalize_catalog(raw: dict) -> dict:
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
                    "metric": column_info.get("metric") or column_info.get("metrica") or "",
                    "semantic_role": column_info.get("semantic_role") or column_info.get("papel") or "",
                    "question_hints": column_info.get("question_hints") or column_info.get("apelidos") or [],
                }
            else:
                columns[column_name] = {"description": column_info}
        foreign_keys = []
        for rel in ensure_list(table_info.get("foreign_keys") or table_info.get("chaves_estrangeiras")):
            if not isinstance(rel, dict):
                continue
            foreign_keys.append(
                {
                    **rel,
                    "references": rel.get("references") or rel.get("referencia"),
                    "referenced_columns": ensure_list(rel.get("referenced_columns") or rel.get("colunas_referenciadas")),
                }
            )
        tables[table_name] = {
            **table_info,
            "description": table_info.get("description") or table_info.get("descricao") or "",
            "primary_key": ensure_list(table_info.get("primary_key") or table_info.get("chave_primaria")),
            "entity_key": ensure_list(table_info.get("entity_key") or table_info.get("chave_negocio")),
            "time_key": table_info.get("time_key") or table_info.get("coluna_tempo"),
            "grain": ensure_list(table_info.get("grain") or table_info.get("grao")),
            "recommended": bool(table_info.get("recommended") if "recommended" in table_info else table_info.get("recomendada")),
            "columns": columns,
            "foreign_keys": foreign_keys,
        }
    return {
        **data,
        "description": data.get("description") or data.get("descricao") or "",
        "tables": tables,
        "intents": {
            {
                "comparar_periodos": "compare_periods",
                "contar_registros": "count_records",
            }.get(intent_name, intent_name): {
                **intent_info,
                "description": intent_info.get("description") or intent_info.get("descricao") or "",
                "triggers": ensure_list(intent_info.get("triggers") or intent_info.get("gatilhos")),
                "comparison_strategy": intent_info.get("comparison_strategy") or intent_info.get("estrategia_comparacao"),
                "required_dimensions": ensure_list(intent_info.get("required_dimensions") or intent_info.get("dimensoes_obrigatorias")),
                "required_entity_key": (
                    intent_info.get("required_entity_key")
                    if "required_entity_key" in intent_info
                    else intent_info.get("exige_chave_negocio")
                ),
                "default_template": intent_info.get("default_template") or intent_info.get("template_padrao"),
                "rules": ensure_list(intent_info.get("rules") or intent_info.get("regras")),
                "default_aggregation": intent_info.get("default_aggregation") or intent_info.get("agregacao_padrao"),
            }
            for intent_name, intent_info in (data.get("intents") or data.get("intencoes") or {}).items()
            if isinstance(intent_info, dict)
        },
        "metrics": {
            metric_name: {
                **metric_info,
                "label": metric_info.get("label") or metric_info.get("rotulo") or "",
                "table": metric_info.get("table") or metric_info.get("tabela"),
                "expression": metric_info.get("expression") or metric_info.get("expressao"),
                "unit": metric_info.get("unit") or metric_info.get("unidade"),
                "description": metric_info.get("description") or metric_info.get("descricao") or "",
                "question_hints": ensure_list(metric_info.get("question_hints") or metric_info.get("apelidos")),
                "filter_semantics": metric_info.get("filter_semantics") or metric_info.get("semantica_filtros") or {},
            }
            for metric_name, metric_info in (data.get("metrics") or data.get("metricas") or {}).items()
            if isinstance(metric_info, dict)
        },
        "examples": data.get("examples") or data.get("exemplos") or [],
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
                "requires": ensure_list(template_info.get("requires") or template_info.get("requer")),
                "allowed_aggregations": ensure_list(template_info.get("allowed_aggregations") or template_info.get("agregacoes_permitidas")),
            }
            for template_name, template_info in (data.get("templates") or data.get("modelos") or {}).items()
            if isinstance(template_info, dict)
        },
    }


def build_table_doc(domain: str, source_file: str, table_name: str, table_info: dict) -> dict:
    columns = table_info.get("columns") or {}
    if isinstance(columns, dict):
        column_names = list(columns.keys())
    elif isinstance(columns, list):
        column_names = [str(item) for item in columns]
    else:
        column_names = []
    text = "\n".join(
        [
            f"Tabela: {table_name}",
            f"Dominio/schema: {domain}",
            f"Descricao: {compact_text(table_info.get('description'))}",
            f"Chave primaria: {', '.join(ensure_list(table_info.get('primary_key')))}",
            f"Logica de negocio: {' | '.join(compact_text(item) for item in ensure_list(table_info.get('logica_negocio')) if compact_text(item))}",
            f"Classificacao por tipo: {summarize_type_classification(table_info)}",
            f"Agrupamentos recomendados: {' | '.join(compact_text(item) for item in ensure_list(table_info.get('agrupamentos_recomendados')) if compact_text(item))}",
            f"Semantica de filtros: {' | '.join(f'{compact_text(name)}: {compact_text(expr)}' for name, expr in (table_info.get('semantica_filtros') or {}).items() if compact_text(name) or compact_text(expr))}",
            f"Colunas: {', '.join(column_names)}",
        ]
    )
    return {
        "id": doc_id("table", table_name),
        "kind": "table",
        "metadata": {
            "domain": domain,
            "schema": domain,
            "source_file": source_file,
            "table": table_name,
            "primary_key": ensure_list(table_info.get("primary_key")),
            "entity_key": ensure_list(table_info.get("entity_key")),
            "time_key": table_info.get("time_key"),
            "recommended": bool(table_info.get("recommended")),
        },
        "text": text,
    }


def build_business_rule_docs(domain: str, source_file: str, table_name: str, table_info: dict) -> list[dict]:
    docs: list[dict] = []

    for index, rule in enumerate(table_business_rules(table_info)):
        docs.append(
            {
                "id": doc_id("business_rule", table_name, str(index), rule),
                "kind": "business_rule",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "rule_type": "business_logic",
                },
                "text": "\n".join(
                    [
                        f"Regra de negocio: {table_name}",
                        f"Tabela: {table_name}",
                        f"Regra: {rule}",
                    ]
                ),
            }
        )

    mapping = table_info.get("classificacao_por_tipo") or table_info.get("type_classification") or {}
    if isinstance(mapping, dict):
        for kind, details in mapping.items():
            if not isinstance(details, dict):
                continue
            text = "\n".join(
                item
                for item in [
                    f"Classificacao por tipo: {table_name}",
                    f"Tabela: {table_name}",
                    f"Tipo: {compact_text(kind)}",
                    f"Coluna origem: {compact_text(details.get('coluna_origem') or details.get('source_column'))}",
                    f"Tabela referencia: {compact_text(details.get('tabela_referencia') or details.get('reference_table'))}",
                    f"Coluna referencia: {compact_text(details.get('coluna_referencia') or details.get('reference_column'))}",
                    f"Coluna descricao: {compact_text(details.get('coluna_descricao') or details.get('description_column'))}",
                    f"Instrucao: {compact_text(details.get('instrucao') or details.get('instruction'))}",
                    f"Quando agrupar: {' | '.join(compact_text(item) for item in ensure_list(details.get('quando_agrupar') or details.get('when_to_group')) if compact_text(item))}",
                ]
                if item
            )
            docs.append(
                {
                    "id": doc_id("classification", table_name, str(kind)),
                    "kind": "classification",
                    "metadata": {
                        "domain": domain,
                        "schema": domain,
                        "source_file": source_file,
                        "table": table_name,
                        "classification": kind,
                        "reference_table": details.get("tabela_referencia") or details.get("reference_table"),
                    },
                    "text": text,
                }
            )

    for name, expression in table_filter_semantics(table_info).items():
        docs.append(
            {
                "id": doc_id("filter_semantics", table_name, str(name)),
                "kind": "filter_semantics",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "filter": name,
                },
                "text": "\n".join(
                    [
                        f"Semantica de filtro: {table_name}",
                        f"Tabela: {table_name}",
                        f"Filtro: {compact_text(name)}",
                        f"Instrucao: {compact_text(expression)}",
                    ]
                ),
            }
        )

    for index, query in enumerate(table_validated_queries(table_info)):
        question = compact_text(query.get("pergunta") or query.get("question"))
        rule = compact_text(query.get("regra") or query.get("rule"))
        sql = compact_text(query.get("sql_exemplo") or query.get("sql"))
        docs.append(
            {
                "id": doc_id("validated_query", table_name, str(index), question),
                "kind": "validated_query",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "question": question,
                },
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
            }
        )

    for index, grouping in enumerate(table_groupings(table_info)):
        docs.append(
            {
                "id": doc_id("grouping_rule", table_name, str(index), grouping),
                "kind": "grouping_rule",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "rule_type": "grouping",
                },
                "text": "\n".join(
                    [
                        f"Agrupamento recomendado: {table_name}",
                        f"Tabela: {table_name}",
                        f"Regra: {grouping}",
                    ]
                ),
            }
        )

    return docs


def build_column_docs(domain: str, source_file: str, table_name: str, table_info: dict) -> list[dict]:
    columns = table_info.get("columns") or {}
    if not isinstance(columns, dict):
        return []

    docs: list[dict] = []
    for column_name, column_info in columns.items():
        column_info = column_info if isinstance(column_info, dict) else {"description": column_info}
        text = "\n".join(
            [
                f"Coluna: {table_name}.{column_name}",
                f"Tabela: {table_name}",
                f"Dominio/schema: {domain}",
                f"Tipo: {column_info.get('type', '')}",
                f"Descricao: {compact_text(column_info.get('description'))}",
            ]
        )
        docs.append(
            {
                "id": doc_id("column", table_name, str(column_name)),
                "kind": "column",
                "metadata": {
                    "column": column_name,
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "type": column_info.get("type", ""),
                    "metric": column_info.get("metric", ""),
                    "semantic_role": column_info.get("semantic_role", ""),
                },
                "text": text,
            }
        )
    return docs


def build_relationship_docs(domain: str, source_file: str, table_name: str, table_info: dict) -> list[dict]:
    docs: list[dict] = []
    for rel in ensure_list(table_info.get("foreign_keys")):
        if not isinstance(rel, dict):
            continue
        text = "\n".join(
            [
                f"Relacionamento: {table_name} -> {rel.get('references', '')}",
                f"Colunas origem: {', '.join(ensure_list(rel.get('columns')))}",
                f"Colunas destino: {', '.join(ensure_list(rel.get('referenced_columns')))}",
                f"Constraint: {rel.get('constraint', '')}",
            ]
        )
        docs.append(
            {
                "id": doc_id("relationship", table_name, rel.get("constraint", "") or ",".join(ensure_list(rel.get("columns")))),
                "kind": "relationship",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "table": table_name,
                    "references": rel.get("references"),
                    "columns": ensure_list(rel.get("columns")),
                    "referenced_columns": ensure_list(rel.get("referenced_columns")),
                },
                "text": text,
            }
        )
    return docs


def build_intent_docs(domain: str, source_file: str, intents: dict) -> list[dict]:
    docs: list[dict] = []
    for intent_name, info in (intents or {}).items():
        if not isinstance(info, dict):
            continue
        text = "\n".join(
            [
                f"Intencao analitica: {intent_name}",
                f"Descricao: {compact_text(info.get('description'))}",
                f"Gatilhos: {', '.join(ensure_list(info.get('triggers')))}",
                f"Estrategia: {info.get('comparison_strategy', '')}",
                f"Template padrao: {info.get('default_template', '')}",
                f"Regras: {' '.join(ensure_list(info.get('rules')))}",
            ]
        )
        docs.append(
            {
                "id": doc_id("intent", domain, str(intent_name)),
                "kind": "intent",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "intent": intent_name,
                    "default_template": info.get("default_template"),
                },
                "text": text,
            }
        )
    return docs


def build_metric_docs(domain: str, source_file: str, metrics: dict) -> list[dict]:
    docs: list[dict] = []
    for metric_name, info in (metrics or {}).items():
        if not isinstance(info, dict):
            continue
        text = "\n".join(
            [
                f"Metrica: {metric_name}",
                f"Label: {compact_text(info.get('label'))}",
                f"Tabela: {info.get('table', '')}",
                f"Expressao: {info.get('expression', '')}",
                f"Unidade: {info.get('unit', '')}",
                f"Dicas de pergunta: {', '.join(ensure_list(info.get('question_hints')))}",
                f"Semantica de filtro: {json.dumps(info.get('filter_semantics', {}), ensure_ascii=False)}",
            ]
        )
        docs.append(
            {
                "id": doc_id("metric", domain, str(metric_name)),
                "kind": "metric",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "metric": metric_name,
                    "table": info.get("table"),
                    "expression": info.get("expression"),
                },
                "text": text,
            }
        )
    return docs


def build_example_docs(domain: str, source_file: str, examples: list) -> list[dict]:
    docs: list[dict] = []
    for index, example in enumerate(examples or []):
        if not isinstance(example, dict):
            continue
        text = "\n".join(
            [
                f"Exemplo de pergunta: {compact_text(example.get('question'))}",
                f"Tabelas: {', '.join(ensure_list(example.get('tables')))}",
                f"Intencao: {example.get('intent', '')}",
                f"Observacao: {compact_text(example.get('note'))}",
            ]
        )
        docs.append(
            {
                "id": doc_id("example", domain, str(index), compact_text(example.get("question"))),
                "kind": "example",
                "metadata": {
                    "domain": domain,
                    "schema": domain,
                    "source_file": source_file,
                    "intent": example.get("intent"),
                    "tables": ensure_list(example.get("tables")),
                },
                "text": text,
            }
        )
    return docs


def main() -> None:
    documents: list[dict] = []
    for path in sorted(CATALOG_DIR.glob("*.json")):
        data = normalize_catalog(json.loads(path.read_text(encoding="utf-8")))
        domain = str(data.get("domain") or path.stem)
        source_file = path.name

        for table_name, table_info in (data.get("tables") or {}).items():
            if not isinstance(table_info, dict):
                continue
            documents.append(build_table_doc(domain, source_file, table_name, table_info))
            documents.extend(build_column_docs(domain, source_file, table_name, table_info))
            documents.extend(build_relationship_docs(domain, source_file, table_name, table_info))
            documents.extend(build_business_rule_docs(domain, source_file, table_name, table_info))

        documents.extend(build_intent_docs(domain, source_file, data.get("intents") or {}))
        documents.extend(build_metric_docs(domain, source_file, data.get("metrics") or {}))
        documents.extend(build_example_docs(domain, source_file, data.get("examples") or []))

    documents.extend(build_markdown_docs())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        for document in documents:
            handle.write(json.dumps(document, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for document in documents:
        kind = str(document.get("kind") or "")
        counts[kind] = counts.get(kind, 0) + 1
    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH),
                "documents": len(documents),
                "kinds": counts,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
