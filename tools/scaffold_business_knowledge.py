from __future__ import annotations

import argparse
import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any

from export_catalog_markdown import normalize_catalog, resolve_user_path, selected_paths


PROJECT_DIR = Path(__file__).resolve().parents[1]


def ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def clean_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def snake(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_") or "sem_nome"


def table_leaf(table_name: str) -> str:
    return table_name.split(".", 1)[-1]


def column_names(info: dict[str, Any]) -> list[str]:
    return list((info.get("colunas") or {}).keys())


def infer_time_candidates(info: dict[str, Any]) -> list[str]:
    candidates = []
    for column in column_names(info):
        lower = column.lower()
        if any(token in lower for token in ("anousu", "exercicio", "ano", "data", "dt")):
            candidates.append(column)
    return candidates[:5]


def infer_active_filter_candidates(table_name: str, info: dict[str, Any]) -> list[str]:
    candidates = []
    for column in column_names(info):
        lower = column.lower()
        full_column = f"{table_name}.{column}"
        if lower in {"ativo", "is_ativo"} or lower.endswith("_ativo"):
            candidates.append(f"Validar se `{full_column} IS TRUE` representa registro ativo.")
        elif any(token in lower for token in ("baixa", "dtbaixa", "dtdemo", "dtexclusao", "cancel", "inativ")):
            candidates.append(f"Validar se `{full_column} IS NULL` representa registro ativo/vigente.")
    return candidates[:5]


def table_score(table_name: str, info: dict[str, Any]) -> int:
    leaf = table_leaf(table_name).lower()
    description = clean_text(info.get("descricao")).lower()
    columns = " ".join(column_names(info)).lower()
    score = 0
    if info.get("recomendada"):
        score += 30
    if ensure_list(info.get("chave_primaria")):
        score += 10
    if ensure_list(info.get("chaves_estrangeiras")):
        score += 8
    if any(token in columns for token in ("matric", "numcgm", "exercicio", "anousu", "valor", "data")):
        score += 8
    if any(token in f"{leaf} {description}" for token in ("base", "cadastro", "mov", "lanc", "calc", "valor")):
        score += 6
    return score


def selected_concept_tables(catalog: dict[str, Any], max_tables: int) -> list[tuple[str, dict[str, Any]]]:
    tables = list((catalog.get("tabelas") or {}).items())
    tables.sort(key=lambda item: (table_score(item[0], item[1]), item[0]), reverse=True)
    return tables[: max(1, max_tables)]


def render_counting_rule(table_name: str, info: dict[str, Any]) -> str:
    entity_key = ensure_list(info.get("chave_negocio"))
    primary_key = ensure_list(info.get("chave_primaria"))
    key = entity_key or primary_key
    if len(key) == 1:
        return f"Para contar entidades, validar se `COUNT(DISTINCT {key[0]})` representa o grao correto."
    if len(key) > 1:
        joined = ", ".join(key)
        return f"Para contar entidades, validar se a combinacao `{joined}` representa o grao correto."
    return "Definir chave de contagem antes de usar `COUNT(1)`."


def render_concepts_markdown(catalog: dict[str, Any], source_file: str, max_tables: int) -> str:
    domain = clean_text(catalog.get("domain")) or Path(source_file).stem
    label = clean_text(catalog.get("rotulo")) or domain
    schema = clean_text(catalog.get("schema_principal")) or domain

    lines = [
        "---",
        f"titulo: Conceitos de negocio - {label}",
        f"dominio: {domain}",
        f"schema_principal: {schema}",
        f"fonte_json: {source_file}",
        "tags:",
        "  - conhecimento-negocio",
        "  - curadoria",
        "  - obsidian",
        "---",
        "",
        f"# Conceitos de negocio - {label}",
        "",
        "Este arquivo e um esqueleto para curadoria humana. Ele nao deve ser usado como verdade final sem revisao do consultor.",
        "",
        "Quando um conceito estiver validado, copie ou adapte a secao para `knowledge/manual/<schema>/conceitos.md` e regenere o RAG.",
        "",
        f"## Conceito de negocio: visao_geral_{snake(schema)}",
        "",
        f"- Nome humano: visao geral do schema {schema}.",
        "- Perguntas comuns:",
        "  - Preencher com perguntas reais do usuario.",
        "- Significado: Preencher com o papel do schema no negocio.",
        "- Entidade principal: Preencher.",
        "- Tabelas envolvidas:",
        "  - Preencher.",
        "- Grao esperado: Preencher.",
        "- Filtros de negocio:",
        "  - Preencher.",
        "- Caminho de negocio:",
        "  - Preencher.",
        "- Regra de contagem: Preencher.",
        "- O que nao inferir:",
        "  - Nao inferir regra de negocio apenas pelo nome tecnico.",
        "- Cuidados:",
        "  - Validar com pessoa de negocio antes de promover para o manual operacional.",
        "",
        "## Candidatos extraidos do catalogo",
        "",
    ]

    for table_name, info in selected_concept_tables(catalog, max_tables):
        leaf = table_leaf(table_name)
        description = clean_text(info.get("descricao")) or leaf
        active_filters = infer_active_filter_candidates(table_name, info)
        time_candidates = infer_time_candidates(info)
        fk_lines = []
        for fk in ensure_list(info.get("chaves_estrangeiras")):
            if not isinstance(fk, dict):
                continue
            columns = ", ".join(ensure_list(fk.get("columns")))
            reference = clean_text(fk.get("referencia"))
            referenced_columns = ", ".join(ensure_list(fk.get("colunas_referenciadas")))
            if columns and reference:
                fk_lines.append(f"`{table_name}.{columns} -> {reference}.{referenced_columns}`")

        lines.extend(
            [
                f"## Conceito de negocio: {snake(leaf)}",
                "",
                f"- Nome humano: {description}.",
                "- Perguntas comuns:",
                f"  - Quantos registros existem em {description}?",
                f"  - Liste {description}.",
                "- Significado: Preencher em linguagem de negocio.",
                f"- Entidade principal: {description}.",
                f"- Fonte primaria: `{table_name}`.",
                "- Tabelas envolvidas:",
                f"  - `{table_name}`",
                f"- Grao esperado: {', '.join(ensure_list(info.get('grao'))) or ', '.join(ensure_list(info.get('chave_primaria'))) or 'Preencher.'}",
                "- Filtros de negocio:",
                *(f"  - {item}" for item in active_filters),
                *(f"  - Candidato a tempo/exercicio: `{table_name}.{column}`." for column in time_candidates),
                *(["  - Preencher."] if not active_filters and not time_candidates else []),
                "- Caminho de negocio:",
                *(f"  - {item}" for item in fk_lines),
                *(["  - Preencher caminhos semanticos que a FK nao explica."] if not fk_lines else []),
                f"- Regra de contagem: {render_counting_rule(table_name, info)}",
                "- O que nao inferir:",
                "  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.",
                "- Cuidados:",
                "  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def relationship_fks(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    seen = set()
    for table_name, info in (catalog.get("tabelas") or {}).items():
        for fk in ensure_list(info.get("chaves_estrangeiras")):
            if not isinstance(fk, dict):
                continue
            reference = clean_text(fk.get("referencia"))
            pairs = []
            for column, referenced_column in zip(
                ensure_list(fk.get("columns")),
                ensure_list(fk.get("colunas_referenciadas")),
            ):
                pair = (clean_text(column), clean_text(referenced_column))
                if pair[0] and pair[1] and pair not in pairs:
                    pairs.append(pair)
            columns = [pair[0] for pair in pairs]
            referenced_columns = [pair[1] for pair in pairs]
            if not reference or not columns or not referenced_columns:
                continue
            key = (table_name, reference, tuple(columns), tuple(referenced_columns))
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "source": table_name,
                    "target": reference,
                    "columns": columns,
                    "referenced_columns": referenced_columns,
                    "constraint": clean_text(fk.get("constraint")),
                }
            )
    return rows


def render_join(source: str, source_columns: list[str], target: str, target_columns: list[str]) -> str:
    pairs = []
    for source_column, target_column in zip(source_columns, target_columns):
        pairs.append(f"`{source}.{source_column} = {target}.{target_column}`")
    return " e ".join(pairs)


def bridge_recipes(fks: list[dict[str, Any]], max_items: int) -> list[list[str]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for fk in fks:
        by_source.setdefault(fk["source"], []).append(fk)

    recipes: list[list[str]] = []
    seen: set[tuple[str, str, str]] = set()
    for bridge, items in sorted(by_source.items()):
        distinct_targets = [item for item in items if item["target"] != bridge]
        if len(distinct_targets) < 2:
            continue
        for left, right in combinations(distinct_targets[:6], 2):
            key = tuple(sorted([left["target"], right["target"]]) + [bridge])
            if key in seen:
                continue
            seen.add(key)
            left_leaf = table_leaf(left["target"])
            right_leaf = table_leaf(right["target"])
            bridge_leaf = table_leaf(bridge)
            recipes.append(
                [
                    f"## Receita de relacionamento: {snake(left_leaf)}_para_{snake(right_leaf)}_via_{snake(bridge_leaf)}",
                    "",
                    "- Tipo: caminho candidato por tabela ponte.",
                    f"- Quando usar: perguntas que precisem relacionar `{left['target']}` com `{right['target']}` usando `{bridge}`.",
                    f"- Origem de negocio: `{left['target']}`.",
                    f"- Destino de negocio: `{right['target']}`.",
                    "- Tabelas no caminho:",
                    f"  - `{left['target']}`",
                    f"  - `{bridge}`",
                    f"  - `{right['target']}`",
                    "- Caminho de negocio:",
                    f"  - {table_leaf(left['target'])} -> {bridge_leaf} -> {table_leaf(right['target'])}",
                    "- Join logico:",
                    f"  - {render_join(bridge, left['columns'], left['target'], left['referenced_columns'])}",
                    f"  - {render_join(bridge, right['columns'], right['target'], right['referenced_columns'])}",
                    "- Cardinalidade: Preencher.",
                    "- Filtros recomendados:",
                    "  - Preencher filtros de negocio.",
                    "- Cuidados:",
                    "  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.",
                    "",
                ]
            )
            if len(recipes) >= max_items:
                return recipes
    return recipes


def direct_recipes(fks: list[dict[str, Any]], remaining: int) -> list[list[str]]:
    recipes = []
    for fk in sorted(fks, key=lambda item: (item["source"], item["target"]))[:remaining]:
        source_leaf = table_leaf(fk["source"])
        target_leaf = table_leaf(fk["target"])
        recipes.append(
            [
                f"## Receita de relacionamento: {snake(source_leaf)}_para_{snake(target_leaf)}",
                "",
                "- Tipo: relacionamento direto por FK catalogada.",
                f"- Quando usar: perguntas que precisem relacionar `{fk['source']}` com `{fk['target']}`.",
                f"- Origem de negocio: `{fk['source']}`.",
                f"- Destino de negocio: `{fk['target']}`.",
                "- Tabelas no caminho:",
                f"  - `{fk['source']}`",
                f"  - `{fk['target']}`",
                "- Caminho de negocio:",
                f"  - {source_leaf} -> {target_leaf}",
                "- Sentidos de uso:",
                f"  - `{fk['source']}` para `{fk['target']}`.",
                f"  - `{fk['target']}` para `{fk['source']}`, quando a pergunta partir da tabela referenciada.",
                "- Join logico:",
                f"  - {render_join(fk['source'], fk['columns'], fk['target'], fk['referenced_columns'])}",
                "- Cardinalidade: Preencher.",
                "- Filtros recomendados:",
                "  - Preencher filtros de negocio.",
                "- Cuidados:",
                "  - FK tecnica nao prova, sozinha, que esse e o melhor caminho de negocio para toda pergunta.",
                "",
            ]
        )
    return recipes


def render_relationships_markdown(catalog: dict[str, Any], source_file: str, max_recipes: int) -> str:
    domain = clean_text(catalog.get("domain")) or Path(source_file).stem
    label = clean_text(catalog.get("rotulo")) or domain
    schema = clean_text(catalog.get("schema_principal")) or domain
    fks = relationship_fks(catalog)
    bridge = bridge_recipes(fks, max_recipes)
    remaining = max(0, max_recipes - len(bridge))
    direct = direct_recipes(fks, remaining)

    lines = [
        "---",
        f"titulo: Relacionamentos de negocio - {label}",
        f"dominio: {domain}",
        f"schema_principal: {schema}",
        f"fonte_json: {source_file}",
        "tags:",
        "  - conhecimento-negocio",
        "  - relacionamentos",
        "  - curadoria",
        "  - obsidian",
        "---",
        "",
        f"# Relacionamentos de negocio - {label}",
        "",
        "Este arquivo e um esqueleto para curadoria humana. Priorize validar caminhos que a FK isolada nao explica.",
        "",
        "Quando uma receita estiver validada, copie ou adapte a secao para `knowledge/manual/<schema>/relacionamentos_negocio.md` e regenere o RAG.",
        "",
        "## Receita de relacionamento: modelo",
        "",
        "- Quando usar: Preencher.",
        "- Origem de negocio: Preencher.",
        "- Destino de negocio: Preencher.",
        "- Tabelas no caminho:",
        "  - Preencher.",
        "- Caminho de negocio:",
        "  - Preencher.",
        "- Join logico:",
        "  - Preencher.",
        "- Cardinalidade: Preencher.",
        "- Filtros recomendados:",
        "  - Preencher.",
        "- Cuidados:",
        "  - Preencher.",
        "",
        "## Receitas candidatas extraidas do catalogo",
        "",
    ]

    for recipe in bridge + direct:
        lines.extend(recipe)

    if len(fks) > max_recipes:
        lines.extend(
            [
                "## Observacao de limite",
                "",
                f"- O catalogo possui {len(fks)} FKs candidatas. Este arquivo gerou no maximo {max_recipes} receitas para revisao inicial.",
                "- Aumente `--max-relationship-recipes` se precisar de mais caminhos brutos.",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def write_output(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        print(f"[business-scaffold] preservado {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[business-scaffold] gravado {path}")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera esqueletos de conceitos e relacionamentos para curadoria.")
    parser.add_argument("--catalog-dir", type=Path, default=Path("../catalog"))
    parser.add_argument("--output-dir", type=Path, default=Path("../docs/exemplos/obsidian"))
    parser.add_argument("--domain", default="all", help="Schema/dominio alvo ou 'all'.")
    parser.add_argument("--max-concept-tables", type=int, default=20)
    parser.add_argument("--max-relationship-recipes", type=int, default=80)
    parser.add_argument("--overwrite", action="store_true", help="Sobrescreve arquivos ja existentes.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog_dir = resolve_user_path(args.catalog_dir)
    output_dir = resolve_user_path(args.output_dir)

    for path in selected_paths(catalog_dir, args.domain):
        if not path.exists():
            raise SystemExit(f"Arquivo nao encontrado: {path}")
        catalog = normalize_catalog(json.loads(path.read_text(encoding="utf-8")))
        stem = path.stem
        write_output(
            output_dir / f"{stem}.conceitos.md",
            render_concepts_markdown(catalog, path.name, args.max_concept_tables),
            args.overwrite,
        )
        write_output(
            output_dir / f"{stem}.relacionamentos_negocio.md",
            render_relationships_markdown(catalog, path.name, args.max_relationship_recipes),
            args.overwrite,
        )


if __name__ == "__main__":
    main()
