from __future__ import annotations

import json
import re
from pathlib import Path

from config import CATALOG_DIR
from services.logger import log_event


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
    def __init__(self, catalog_dir: Path = CATALOG_DIR):
        self.catalog_dir = catalog_dir
        self.data = self._load()

    def _load(self) -> dict:
        domains = []
        tables = {}
        examples = []
        intents = {}
        metrics = {}
        templates = {}
        table_sources = {}

        for path in sorted(self.catalog_dir.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                data = self._normalize_catalog(json.load(handle))

            domains.append(
                {
                    "domain": data.get("domain") or path.stem,
                    "label": data.get("label") or path.stem,
                    "description": data.get("description", ""),
                    "primary_schema": data.get("primary_schema"),
                }
            )
            file_tables = data.get("tables", {})
            log_event(
                "catalog.load_file",
                {
                    "file": path.name,
                    "domain": data.get("domain") or path.stem,
                    "tables": len(file_tables),
                },
            )
            for table_name, table_info in file_tables.items():
                if table_name in tables:
                    log_event(
                        "catalog.duplicate_table",
                        {
                            "table": table_name,
                            "previous_file": table_sources.get(table_name),
                            "current_file": path.name,
                        },
                    )
                tables[table_name] = table_info
                table_sources[table_name] = path.name
            examples.extend(data.get("examples", []))
            intents.update(data.get("intents", {}))
            metrics.update(data.get("metrics", {}))
            templates.update(data.get("templates", {}))

        log_event(
            "catalog.loaded",
            {
                "files": len(domains),
                "tables": len(tables),
                "intents": len(intents),
                "metrics": len(metrics),
                "templates": len(templates),
            },
        )

        return {
            "domain": "ecidade",
            "label": "e-Cidade",
            "description": "Catalogo consolidado de dominios do e-Cidade.",
            "domains": domains,
            "intents": intents,
            "metrics": metrics,
            "templates": templates,
            "tables": tables,
            "examples": examples,
        }

    def _normalize_catalog(self, raw: dict) -> dict:
        data = dict(raw or {})
        tables = {}
        for table_name, table_info in (data.get("tables") or data.get("tabelas") or {}).items():
            tables[table_name] = self._normalize_table(table_info)
        metrics = {}
        for metric_name, metric_info in (data.get("metrics") or data.get("metricas") or {}).items():
            if not isinstance(metric_info, dict):
                continue
            metrics[metric_name] = {
                **metric_info,
                "label": metric_info.get("label") or metric_info.get("rotulo") or "",
                "table": metric_info.get("table") or metric_info.get("tabela"),
                "expression": metric_info.get("expression") or metric_info.get("expressao"),
                "unit": metric_info.get("unit") or metric_info.get("unidade"),
                "description": metric_info.get("description") or metric_info.get("descricao") or "",
                "question_hints": metric_info.get("question_hints") or metric_info.get("apelidos") or [],
                "filter_semantics": metric_info.get("filter_semantics") or metric_info.get("semantica_filtros") or {},
            }
        intents = {}
        intent_name_map = {
            "comparar_periodos": "compare_periods",
            "contar_registros": "count_records",
        }
        for raw_intent_name, intent_info in (data.get("intents") or data.get("intencoes") or {}).items():
            if not isinstance(intent_info, dict):
                continue
            intent_name = intent_name_map.get(raw_intent_name, raw_intent_name)
            intents[intent_name] = {
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
        templates = {}
        template_name_map = {
            "comparar_periodos_mesma_entidade": "compare_periods_same_entity",
        }
        for raw_template_name, template_info in (data.get("templates") or data.get("modelos") or {}).items():
            if not isinstance(template_info, dict):
                continue
            template_name = template_name_map.get(raw_template_name, raw_template_name)
            templates[template_name] = {
                **template_info,
                "intent": {
                    "comparar_periodos": "compare_periods",
                    "contar_registros": "count_records",
                }.get(template_info.get("intent") or template_info.get("intencao"), template_info.get("intent") or template_info.get("intencao")),
                "strategy": template_info.get("strategy") or template_info.get("estrategia"),
                "requires": template_info.get("requires") or template_info.get("requer") or [],
                "allowed_aggregations": template_info.get("allowed_aggregations") or template_info.get("agregacoes_permitidas") or [],
            }

        return {
            **data,
            "label": data.get("label") or data.get("rotulo") or data.get("domain"),
            "description": data.get("description") or data.get("descricao") or "",
            "primary_schema": data.get("primary_schema") or data.get("schema_principal"),
            "intents": intents,
            "metrics": metrics,
            "templates": templates,
            "tables": tables,
            "examples": data.get("examples") or data.get("exemplos") or [],
        }

    def _normalize_table(self, raw: dict) -> dict:
        info = dict(raw or {})
        columns = {}
        for column_name, column_info in (info.get("columns") or info.get("colunas") or {}).items():
            columns[column_name] = self._normalize_column(column_info)

        foreign_keys = []
        for fk in (info.get("foreign_keys") or info.get("chaves_estrangeiras") or []):
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
            "primary_key": info.get("primary_key") or info.get("chave_primaria") or [],
            "grain": info.get("grain") or info.get("grao") or [],
            "entity_key": info.get("entity_key") or info.get("chave_negocio") or [],
            "time_key": info.get("time_key") or info.get("coluna_tempo"),
            "default_filters": info.get("default_filters") or info.get("filtros_padrao") or [],
            "foreign_keys": foreign_keys,
            "blocked_columns": info.get("blocked_columns") or info.get("colunas_bloqueadas") or [],
            "blocked": bool(info.get("blocked") if "blocked" in info else info.get("bloqueada")),
            "recommended": bool(info.get("recommended") if "recommended" in info else info.get("recomendada")),
            "business_logic": info.get("business_logic") or info.get("logica_negocio") or [],
            "filter_semantics": info.get("filter_semantics") or info.get("semantica_filtros") or {},
            "type_classification": info.get("type_classification") or info.get("classificacao_por_tipo") or {},
            "recommended_groupings": info.get("recommended_groupings") or info.get("agrupamentos_recomendados") or [],
            "validated_queries": info.get("validated_queries") or info.get("consultas_validadas") or [],
            "business_notes": info.get("business_notes") or info.get("observacoes_negocio") or [],
            "columns": columns,
        }

    def _normalize_column(self, raw: object) -> dict:
        if not isinstance(raw, dict):
            return {"description": raw}
        info = dict(raw)
        return {
            **info,
            "description": info.get("description") or info.get("descricao") or "",
            "type": info.get("type") or info.get("tipo"),
            "semantic_role": info.get("semantic_role") or info.get("papel") or "",
            "metric": info.get("metric") or info.get("metrica") or "",
            "question_hints": info.get("question_hints") or info.get("apelidos") or [],
        }

    def schemas(self) -> list[str]:
        schemas = set()
        for table_name in self.table_names():
            if "." in table_name:
                schemas.add(table_name.split(".", 1)[0])
        return sorted(schemas)

    def table_names(self) -> list[str]:
        return sorted(self.data.get("tables", {}).keys())

    def has_table(self, schema: str, table: str) -> bool:
        return f"{schema}.{table}" in self.data.get("tables", {})

    def table(self, schema: str, table: str) -> dict:
        return self.data.get("tables", {}).get(f"{schema}.{table}", {})

    def index(self) -> dict:
        tables = {}
        for name, info in self.data.get("tables", {}).items():
            tables[name] = {
                "description": info.get("description"),
                "primary_key": info.get("primary_key", []),
                "grain": info.get("grain", []),
                "entity_key": info.get("entity_key", []),
                "time_key": info.get("time_key"),
                "default_filters": info.get("default_filters", []),
                "foreign_keys": info.get("foreign_keys", []),
                "known_columns": info.get("columns", {}),
                "blocked_columns": info.get("blocked_columns", []),
                "blocked": bool(info.get("blocked")),
                "recommended": bool(info.get("recommended")),
                "business_logic": info.get("business_logic", []),
                "filter_semantics": info.get("filter_semantics", {}),
                "type_classification": info.get("type_classification", {}),
                "recommended_groupings": info.get("recommended_groupings", []),
                "validated_queries": info.get("validated_queries", []),
                "business_notes": info.get("business_notes", []),
            }

        return {
            "domain": self.data.get("domain"),
            "label": self.data.get("label"),
            "description": self.data.get("description"),
            "schemas": self.schemas(),
            "domains": self.data.get("domains", []),
            "intents": self.data.get("intents", {}),
            "metrics": self.data.get("metrics", {}),
            "templates": self.data.get("templates", {}),
            "tables": tables,
            "examples": self.data.get("examples", []),
        }

    def search(self, text: str, limit: int = 20) -> list[dict]:
        terms = self._search_terms(text)
        results = []
        for full_name, info in self.data.get("tables", {}).items():
            if bool(info.get("blocked")):
                continue
            score = self._score_table(full_name, info, terms)
            if not terms or score:
                results.append(
                    {
                    "table": full_name,
                    "description": info.get("description"),
                    "columns": info.get("columns", {}),
                    "grain": info.get("grain", []),
                    "entity_key": info.get("entity_key", []),
                    "time_key": info.get("time_key"),
                    "default_filters": info.get("default_filters", []),
                    "blocked": bool(info.get("blocked")),
                    "recommended": bool(info.get("recommended")),
                    "score": score,
                }
                )
        results.sort(key=lambda item: (item["score"], item["recommended"]), reverse=True)
        return results[: max(1, min(int(limit or 20), 100))]

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
        columns = info.get("columns", {})
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
