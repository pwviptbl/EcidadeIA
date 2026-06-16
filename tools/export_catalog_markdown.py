from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent


def ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def text(value: Any) -> str:
    return " ".join(str(value or "").split())


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
                    "descricao": column_info.get("descricao") or column_info.get("description") or "",
                    "tipo": column_info.get("tipo") or column_info.get("type") or "",
                    "papel": column_info.get("papel") or column_info.get("semantic_role") or "",
                    "metrica": column_info.get("metrica") or column_info.get("metric") or "",
                    "apelidos": ensure_list(column_info.get("apelidos") or column_info.get("question_hints")),
                    "semantica_filtros": column_info.get("semantica_filtros") or column_info.get("filter_semantics") or {},
                }
            else:
                columns[column_name] = {"descricao": text(column_info), "tipo": "", "papel": "", "metrica": ""}
        foreign_keys = []
        for fk in ensure_list(table_info.get("chaves_estrangeiras") or table_info.get("foreign_keys")):
            if not isinstance(fk, dict):
                continue
            foreign_keys.append(
                {
                    **fk,
                    "referencia": fk.get("referencia") or fk.get("references") or "",
                    "colunas_referenciadas": ensure_list(
                        fk.get("colunas_referenciadas") or fk.get("referenced_columns")
                    ),
                }
            )
        tables[table_name] = {
            **table_info,
            "descricao": table_info.get("descricao") or table_info.get("description") or "",
            "chave_primaria": ensure_list(table_info.get("chave_primaria") or table_info.get("primary_key")),
            "grao": ensure_list(table_info.get("grao") or table_info.get("grain")),
            "chave_negocio": ensure_list(table_info.get("chave_negocio") or table_info.get("entity_key")),
            "coluna_tempo": table_info.get("coluna_tempo") or table_info.get("time_key"),
            "filtros_padrao": ensure_list(table_info.get("filtros_padrao") or table_info.get("default_filters")),
            "recomendada": bool(
                table_info.get("recomendada") if "recomendada" in table_info else table_info.get("recommended")
            ),
            "apelidos": ensure_list(table_info.get("apelidos") or table_info.get("question_hints")),
            "significado_contagem": table_info.get("significado_contagem") or table_info.get("count_meaning") or "",
            "semantica_filtros": table_info.get("semantica_filtros") or table_info.get("filter_semantics") or {},
            "colunas": columns,
            "chaves_estrangeiras": foreign_keys,
        }
    return {
        **data,
        "domain": data.get("domain") or "",
        "rotulo": data.get("rotulo") or data.get("label") or data.get("domain") or "",
        "descricao": data.get("descricao") or data.get("description") or "",
        "schema_principal": data.get("schema_principal") or data.get("primary_schema") or "",
        "metricas": data.get("metricas") or data.get("metrics") or {},
        "intencoes": data.get("intencoes") or data.get("intents") or {},
        "exemplos": data.get("exemplos") or data.get("examples") or [],
        "tabelas": tables,
    }


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def infer_time_candidates(columns: dict[str, Any]) -> list[str]:
    candidates = []
    for name, info in columns.items():
        haystack = f"{name} {text(info.get('descricao'))}".lower()
        if any(token in haystack for token in ("anousu", "exercicio", "ano", "data", "dt")):
            candidates.append(name)
    return candidates[:5]


def infer_business_key_candidates(columns: dict[str, Any]) -> list[str]:
    candidates = []
    for name, info in columns.items():
        haystack = f"{name} {text(info.get('descricao'))}".lower()
        if any(token in haystack for token in ("matric", "numcgm", "inscr", "codigo", "id", "sequencial")):
            candidates.append(name)
    return candidates[:5]


def infer_question_suggestions(table_name: str, info: dict[str, Any]) -> list[str]:
    suggestions = [text(item) for item in ensure_list(info.get("apelidos")) if text(item)]
    leaf = table_name.split(".", 1)[-1].lower()
    description = text(info.get("descricao")).lower()

    if not suggestions and "rua" in leaf:
        suggestions.extend(["quantas ruas temos?", "quais ruas estao cadastradas?"])
    if not suggestions and "iptucalc" in leaf:
        suggestions.extend(["compare o IPTU entre anos", "quais fatores explicam aumento do IPTU?"])
    if not suggestions and "iptucalv" in leaf:
        suggestions.extend(["qual a soma do IPTU por ano?", "qual o valor gerado de IPTU?"])
    if not suggestions and "iptubase" in leaf:
        suggestions.extend(["quantos imoveis temos?", "quais imoveis estao ativos?"])
    if not suggestions and "histor" in description:
        suggestions.extend(["quais tipos de historico existem?", "como classificar os valores do IPTU?"])

    return suggestions[:6]


def render_type_classification(info: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    mapping = info.get("classificacao_por_tipo") or {}
    if not isinstance(mapping, dict):
        return lines
    for kind, details in mapping.items():
        if not isinstance(details, dict):
            continue
        summary = []
        for key in ("coluna_origem", "coluna_chave", "tabela_referencia", "coluna_referencia", "coluna_descricao"):
            value = text(details.get(key))
            if value:
                summary.append(f"{key}={value}")
        instruction = text(details.get("instrucao"))
        base = f"- `{kind}`"
        if summary:
            base += f": {', '.join(summary)}"
        if instruction:
            base += f". {instruction}"
        lines.append(base)
        for item in ensure_list(details.get("quando_agrupar")):
            item_text = text(item)
            if item_text:
                lines.append(f"  - agrupar quando: {item_text}")
    return lines


def render_table_section(table_name: str, info: dict[str, Any]) -> str:
    fk_lines = []
    for fk in info.get("chaves_estrangeiras") or []:
        origem = ", ".join(ensure_list(fk.get("columns")))
        destino = ", ".join(ensure_list(fk.get("colunas_referenciadas")))
        referencia = text(fk.get("referencia"))
        constraint = text(fk.get("constraint"))
        fk_lines.append(f"- `{origem}` -> `{referencia}` ({destino})" + (f" [{constraint}]" if constraint else ""))

    filtro_items = info.get("semantica_filtros") or {}
    filtro_lines = [f"- {nome}: `{expr}`" for nome, expr in filtro_items.items()]
    filtro_padrao_lines = [f"- `{item}`" for item in ensure_list(info.get("filtros_padrao")) if text(item)]
    business_logic_lines = [f"- {text(item)}" for item in ensure_list(info.get("logica_negocio")) if text(item)]
    time_candidates = infer_time_candidates(info.get("colunas") or {})
    business_key_candidates = infer_business_key_candidates(info.get("colunas") or {})
    primary_key = ensure_list(info.get("chave_primaria"))
    entity_key = ensure_list(info.get("chave_negocio")) or primary_key
    time_key = text(info.get("coluna_tempo")) or (time_candidates[0] if time_candidates else "")
    metric_lines = []
    dimension_lines = []
    for column_name, column_info in sorted((info.get("colunas") or {}).items()):
        role = text(column_info.get("papel")).lower()
        metric = text(column_info.get("metrica"))
        description = text(column_info.get("descricao"))
        line = f"- `{column_name}`"
        if description:
            line += f": {description}"
        if metric or any(token in f"{column_name} {role} {description}".lower() for token in ("valor", "area", "quant", "aliq", "perc", "total")):
            metric_lines.append(line)
        elif any(token in f"{column_name} {role} {description}".lower() for token in ("codigo", "matric", "bairro", "setor", "tipo", "grupo", "data", "ano")):
            dimension_lines.append(line)

    section = [
        f"## Tabela de negocio: `{table_name}`",
        "",
        "### Identidade",
        "",
        f"- Nome humano: {text(info.get('descricao')) or table_name}.",
        f"- O que representa: {text(info.get('descricao')) or 'Preencher em linguagem de negocio.'}",
        "- Quando usar:",
        "  - Preencher com perguntas/casos de negocio.",
        "- Quando evitar:",
        "  - Preencher com tabelas ou cenarios mais adequados.",
        "",
        "### Grao e chaves",
        "",
        f"- Grao: {', '.join(ensure_list(info.get('grao'))) or 'Preencher.'}",
        "- Entidade principal: Preencher.",
        "- Chave de negocio:",
        *(f"  - `{item}`" for item in entity_key),
        *(["  - Preencher."] if not entity_key else []),
        f"- Coluna temporal: `{time_key}`" if time_key else "- Coluna temporal: Preencher.",
        f"- Candidatas a chave de negocio: {', '.join(business_key_candidates) or 'Nenhuma inferida automaticamente.'}",
        f"- Candidatas a coluna temporal: {', '.join(time_candidates) or 'Nenhuma inferida automaticamente.'}",
        "",
        "### Colunas principais",
        "",
        *(
            f"- `{column_name}`: {text(column_info.get('descricao')) or 'Preencher significado.'}"
            for column_name, column_info in sorted((info.get("colunas") or {}).items())
        ),
        "",
        "### Metricas atomicas",
        "",
        *(metric_lines or ["- Preencher apenas se houver coluna numerica com significado de negocio."]),
        "",
        "### Dimensoes",
        "",
        *(dimension_lines or ["- Preencher dimensoes de agrupamento/filtro."]),
        "",
        "### Filtros de negocio",
        "",
        *(filtro_padrao_lines or filtro_lines or ["- Preencher filtros obrigatorios ou comuns."]),
        "",
        "### Regra de contagem",
        "",
        f"- {text(info.get('significado_contagem')) or 'Definir o que uma linha representa antes de contar.'}",
        "- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.",
        "",
        "### Regra de agregacao",
        "",
        "- Preencher como somar, contar ou agrupar sem mudar o grao.",
        "",
        "### Relacionamentos importantes",
        "",
        *(fk_lines or ["- Nenhum relacionamento catalogado."]),
        "",
        "### Regras de negocio existentes no catalogo",
        "",
        *(business_logic_lines or ["- Preencher regras validadas por pessoa de negocio."]),
        "",
        "### Riscos de duplicidade",
        "",
        "- Preencher onde joins podem multiplicar linhas ou valores.",
        "",
        "### O que nao inferir",
        "",
        "- Nao inferir regra de negocio apenas pelo nome tecnico.",
        "",
        "### Cuidados",
        "",
        *([f"- {text(item)}" for item in ensure_list(info.get("observacoes_negocio")) if text(item)] or ["- Preencher ambiguidades, excecoes e limites conhecidos."]),
        "",
    ]
    return "\n".join(section)


def render_domain_markdown(catalog: dict[str, Any], source_file: str) -> str:
    domain = text(catalog.get("domain"))
    rotulo = text(catalog.get("rotulo")) or domain
    descricao = text(catalog.get("descricao"))
    schema = text(catalog.get("schema_principal"))
    table_names = sorted((catalog.get("tabelas") or {}).keys())

    lines = [
        "---",
        f"titulo: Catalogo {rotulo}",
        f"dominio: {domain}",
        f"schema_principal: {schema}",
        f"fonte_json: {source_file}",
        "tags:",
        "  - catalogo",
        "  - ecidade",
        f"  - {domain}",
        "---",
        "",
        f"# Catalogo {rotulo}",
        "",
        f"- Dominio: `{domain}`",
        f"- Schema principal: `{schema}`" if schema else "- Schema principal: ",
        f"- Arquivo origem: `{source_file}`",
        f"- Descricao: {descricao or 'Preencher.'}",
        "",
        "## Como usar esta nota",
        "",
        "- Esta nota preserva a estrutura tecnica do catalogo.",
        "- O objetivo e enriquecer regra de negocio em linguagem humana.",
        "- Preencha principalmente os blocos de perguntas, regras, filtros e cuidados.",
        "",
        "## Tabelas deste dominio",
        "",
        *(f"- `{table_name}`" for table_name in table_names),
        "",
    ]

    for table_name in table_names:
        lines.append(render_table_section(table_name, catalog["tabelas"][table_name]))

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta catálogos JSON para Markdown amigável para Obsidian.")
    parser.add_argument("--catalog-dir", type=Path, default=Path("../catalog"))
    parser.add_argument("--output-dir", type=Path, default=Path("../docs/exemplos/obsidian"))
    parser.add_argument("--domain", default="all", help="Schema/dominio alvo ou 'all'.")
    return parser.parse_args()


def resolve_user_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    candidates = [
        (PROJECT_DIR / path),
        (Path.cwd() / path),
        (BASE_DIR / path),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (PROJECT_DIR / path).resolve()


def selected_paths(catalog_dir: Path, domain: str) -> list[Path]:
    if domain.lower() == "all":
        return sorted(catalog_dir.glob("*.json"))
    candidates = [
        catalog_dir / f"{domain}.json",
        catalog_dir / f"{domain}_extraido.json",
    ]
    existing = [path for path in candidates if path.exists()]
    if existing:
        return existing
    return sorted(catalog_dir.glob(f"{domain}*.json")) or [catalog_dir / f"{domain}.json"]


def main() -> None:
    args = parse_args()
    catalog_dir = resolve_user_path(args.catalog_dir)
    output_dir = resolve_user_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in selected_paths(catalog_dir, args.domain):
        if not path.exists():
            raise SystemExit(f"Arquivo nao encontrado: {path}")
        raw = json.loads(path.read_text(encoding="utf-8"))
        catalog = normalize_catalog(raw)
        markdown = render_domain_markdown(catalog, path.name)
        output_path = output_dir / f"{path.stem}.catalogo.md"
        output_path.write_text(markdown, encoding="utf-8")
        print(output_path)


if __name__ == "__main__":
    main()
