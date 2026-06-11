from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TOP_LEVEL_MAP = {
    "label": "rotulo",
    "description": "descricao",
    "primary_schema": "schema_principal",
    "tables": "tabelas",
    "metrics": "metricas",
    "intents": "intencoes",
    "examples": "exemplos",
}

TABLE_MAP = {
    "description": "descricao",
    "primary_key": "chave_primaria",
    "grain": "grao",
    "entity_key": "chave_negocio",
    "time_key": "coluna_tempo",
    "default_filters": "filtros_padrao",
    "recommended": "recomendada",
    "columns": "colunas",
    "foreign_keys": "chaves_estrangeiras",
    "blocked_columns": "colunas_bloqueadas",
    "blocked": "bloqueada",
    "question_hints": "apelidos",
    "count_meaning": "significado_contagem",
    "business_entity": "entidade_negocio",
}

COLUMN_MAP = {
    "description": "descricao",
    "type": "tipo",
    "semantic_role": "papel",
    "metric": "metrica",
    "question_hints": "apelidos",
}

FK_MAP = {
    "references": "referencia",
    "referenced_columns": "colunas_referenciadas",
}

INTENT_MAP = {
    "description": "descricao",
    "triggers": "gatilhos",
    "comparison_strategy": "estrategia_comparacao",
    "required_dimensions": "dimensoes_obrigatorias",
    "required_entity_key": "exige_chave_negocio",
    "default_template": "template_padrao",
    "rules": "regras",
    "default_aggregation": "agregacao_padrao",
}

METRIC_MAP = {
    "label": "rotulo",
    "table": "tabela",
    "expression": "expressao",
    "unit": "unidade",
    "description": "descricao",
    "question_hints": "apelidos",
    "filter_semantics": "semantica_filtros",
}

EXAMPLE_MAP = {
    "question": "pergunta",
    "answer": "resposta",
    "note": "observacao",
}

TEMPLATE_MAP = {
    "intent": "intencao",
    "strategy": "estrategia",
    "requires": "requer",
    "allowed_aggregations": "agregacoes_permitidas",
}


def rename_keys(data: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    converted = {}
    for key, value in data.items():
        converted[mapping.get(key, key)] = value
    return converted


def convert_column(column: Any) -> Any:
    if not isinstance(column, dict):
        return column
    return rename_keys(column, COLUMN_MAP)


def convert_fk(item: Any) -> Any:
    if not isinstance(item, dict):
        return item
    return rename_keys(item, FK_MAP)


def convert_table(table: Any) -> Any:
    if not isinstance(table, dict):
        return table
    converted = rename_keys(table, TABLE_MAP)
    if isinstance(converted.get("colunas"), dict):
        converted["colunas"] = {
            name: convert_column(info) for name, info in converted["colunas"].items()
        }
    if isinstance(converted.get("chaves_estrangeiras"), list):
        converted["chaves_estrangeiras"] = [convert_fk(item) for item in converted["chaves_estrangeiras"]]
    return converted


def convert_metric(metric: Any) -> Any:
    if not isinstance(metric, dict):
        return metric
    return rename_keys(metric, METRIC_MAP)


def convert_intent(intent: Any) -> Any:
    if not isinstance(intent, dict):
        return intent
    converted = rename_keys(intent, INTENT_MAP)
    if converted.get("estrategia_comparacao") == "same_entity":
        converted["estrategia_comparacao"] = "mesma_entidade"
    if converted.get("template_padrao") == "compare_periods_same_entity":
        converted["template_padrao"] = "comparar_periodos_mesma_entidade"
    if converted.get("agregacao_padrao") == "count":
        converted["agregacao_padrao"] = "contagem"
    if isinstance(converted.get("dimensoes_obrigatorias"), list):
        converted["dimensoes_obrigatorias"] = [
            "tempo" if item == "time" else item for item in converted["dimensoes_obrigatorias"]
        ]
    if isinstance(converted.get("gatilhos"), list):
        converted["gatilhos"] = [item for item in converted["gatilhos"] if item != "compare"]
    if isinstance(converted.get("regras"), list):
        converted["regras"] = [
            str(item).replace("entity_key", "chave_negocio")
            for item in converted["regras"]
        ]
    return converted


def convert_example(example: Any) -> Any:
    if not isinstance(example, dict):
        return example
    return rename_keys(example, EXAMPLE_MAP)


def convert_template(template: Any) -> Any:
    if not isinstance(template, dict):
        return template
    converted = rename_keys(template, TEMPLATE_MAP)
    if converted.get("estrategia") == "self_join_same_table":
        converted["estrategia"] = "autojuncao_mesma_tabela"
    if isinstance(converted.get("agregacoes_permitidas"), list):
        translated = []
        for item in converted["agregacoes_permitidas"]:
            translated.append(
                {
                    "count": "contagem",
                    "avg_delta": "media_delta",
                    "sum_delta": "soma_delta",
                    "avg_period": "media_periodo",
                }.get(item, item)
            )
        converted["agregacoes_permitidas"] = translated
    return converted


def convert_catalog(data: dict[str, Any]) -> dict[str, Any]:
    converted = rename_keys(data, TOP_LEVEL_MAP)
    if isinstance(converted.get("tabelas"), dict):
        converted["tabelas"] = {name: convert_table(info) for name, info in converted["tabelas"].items()}
    if isinstance(converted.get("metricas"), dict):
        converted["metricas"] = {name: convert_metric(info) for name, info in converted["metricas"].items()}
    if isinstance(converted.get("intencoes"), dict):
        converted["intencoes"] = {
            {
                "compare_periods": "comparar_periodos",
                "count_records": "contar_registros",
            }.get(name, name): convert_intent(info)
            for name, info in converted["intencoes"].items()
        }
    if isinstance(converted.get("exemplos"), list):
        converted["exemplos"] = [convert_example(item) for item in converted["exemplos"]]
    if isinstance(converted.get("templates"), dict):
        converted["templates"] = {
            {
                "compare_periods_same_entity": "comparar_periodos_mesma_entidade",
            }.get(name, name): convert_template(info)
            for name, info in converted["templates"].items()
        }
    return converted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Converte catálogos JSON existentes para chaves em pt-BR.")
    parser.add_argument("--catalog-dir", type=Path, default=Path("../catalog"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in sorted(args.catalog_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        converted = convert_catalog(data)
        path.write_text(json.dumps(converted, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path.name)


if __name__ == "__main__":
    main()
