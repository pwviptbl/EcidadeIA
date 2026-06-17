from __future__ import annotations

from typing import Any

from agente_v2.context import compact_context
from agente_v2.contracts.normalization import (
    normalize_filter,
    normalize_join,
    normalize_metric,
    resolve_grain_item,
    resolve_named_item,
    split_qualified_ref,
)
from agente_v2.contracts.models import IntentSpec, StageResult
from agente_v2.infrastructure.llm import LLMClient, LLMError
from agente_v2.infrastructure.logger import log_event


class SchemaPlanner:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, question: str, intent: IntentSpec, business: dict, context: dict[str, Any]) -> StageResult:
        payload = {
            "task": (
                "Monte um plano de esquema para responder a pergunta. "
                "Escolha tabelas, grao, eixo temporal, joins e agrupamentos. "
                "Nao escreva SQL. Use colunas reais no grain e filtros estruturados. "
                "Os operadores permitidos sao EXCLUSIVAMENTE: EQUALS, NOT_EQUALS, GREATER_THAN, LESS_THAN, IN, IS_NULL, IS_NOT_NULL. NUNCA invente outros como CONTAINS_CASE_INSENSITIVE. "
                "Nao use condition com SQL bruto."
            ),
            "question": question,
            "intent_spec": intent.to_dict(),
            "business_spec": business,
            "context": compact_context(context),
            "response_schema": {
                "entity": "entidade principal",
                "grain": [],
                "time_axis": {"table": "schema.tabela", "column": "coluna"},
                "tables": [],
                "joins": [
                    {
                        "source_table": "schema.tabela_a",
                        "source_columns": ["coluna_a"],
                        "target_table": "schema.tabela_b",
                        "target_columns": ["coluna_b"],
                        "join_type": "INNER JOIN"
                    }
                ],
                "group_by": [],
                "metrics": [{"metric_name": "nome", "table": "opcional", "column": "opcional", "aggregation": "opcional", "custom_expression": "opcional_formula_sql"}],
                "filters": [],
                "risks": [],
                "open_questions": [],
            },
        }
        try:
            result = self.llm.json(_SYSTEM, payload)
        except LLMError as exc:
            log_event("schema_planner.llm_error", {"error": str(exc)})
            return StageResult("SchemaPlanner", self._fallback(context), [str(exc)])
        sanitized = self._sanitize(result, business)
        log_event("schema_planner.done", sanitized)
        return StageResult("SchemaPlanner", sanitized)

    def _fallback(self, context: dict[str, Any]) -> dict:
        tables = context.get("tables") or []
        return {
            "entity": "",
            "grain": [],
            "time_axis": {},
            "tables": tables[:6],
            "joins": [],
            "group_by": [],
            "metrics": [],
            "filters": [],
            "risks": ["SchemaPlanner usou fallback; plano incompleto."],
            "open_questions": ["Validar grao, metricas, filtros e joins."],
        }

    def _sanitize(self, result: dict, business: dict) -> dict:
        business_metrics = [normalize_metric(item) for item in (business.get("metrics") or []) if isinstance(item, dict)]
        business_filters = [normalize_filter(item) for item in (business.get("filters") or []) if isinstance(item, dict)]
        business_dimensions = [item for item in (business.get("dimensions") or []) if isinstance(item, dict)]
        time_axis = self._normalize_time_axis(result.get("time_axis"))
        metrics = self._normalize_metrics(result.get("metrics") or [], business_metrics)
        filters = self._normalize_filters(result.get("filters") or [], business_filters)
        group_by = self._normalize_group_by(result.get("group_by") or [], business_dimensions, time_axis)
        grain = self._normalize_grain(result.get("grain") or [], business_dimensions, time_axis)
        return {
            "entity": str(result.get("entity") or ""),
            "grain": grain,
            "time_axis": time_axis,
            "tables": self._normalize_tables(result.get("tables") or [], metrics, filters, group_by, grain, time_axis),
            "joins": [normalize_join(item) for item in (result.get("joins") or []) if isinstance(item, dict)],
            "group_by": group_by,
            "metrics": [item for item in metrics if item],
            "filters": [item for item in filters if item],
            "risks": result.get("risks") if isinstance(result.get("risks"), list) else [],
            "open_questions": result.get("open_questions") if isinstance(result.get("open_questions"), list) else [],
        }

    def _normalize_metrics(self, items: list[Any], business_metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for index, item in enumerate(items):
            resolved = resolve_named_item(item, business_metrics, "metric_name")
            normalized = normalize_metric(resolved)
            if not normalized and index < len(business_metrics):
                normalized = dict(business_metrics[index])
            elif index < len(business_metrics):
                normalized = self._merge_missing_fields(normalized, business_metrics[index])
            if normalized:
                output.append(normalized)
        return output

    def _normalize_filters(self, items: list[Any], business_filters: list[dict[str, Any]]) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for index, item in enumerate(items):
            resolved = resolve_named_item(item, business_filters, "filter_name")
            normalized = normalize_filter(resolved)
            if not normalized and index < len(business_filters):
                normalized = dict(business_filters[index])
            elif index < len(business_filters):
                normalized = self._merge_missing_fields(normalized, business_filters[index])
            if normalized:
                output.append(normalized)
        return output

    def _merge_missing_fields(self, item: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
        merged = dict(fallback)
        merged.update({key: value for key, value in item.items() if value not in ("", None, [], {})})
        return merged

    def _normalize_time_axis(self, value: Any) -> dict[str, str]:
        if not isinstance(value, dict):
            return {}
        table = str(value.get("table") or "").strip()
        column = str(value.get("column") or "").strip()
        if not table and "." in column:
            table, column = split_qualified_ref(column)
        return {"table": table, "column": column} if table and column else {}

    def _normalize_group_by(self, items: list[Any], business_dimensions: list[dict], time_axis: dict[str, Any]) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for item in items:
            resolved = resolve_named_item(item, business_dimensions, "dimension_name")
            if isinstance(resolved, str) and "." in resolved:
                table, column = split_qualified_ref(resolved)
                if table and column:
                    output.append({"table": table, "column": column})
                    continue
            if isinstance(resolved, dict):
                table = str(resolved.get("table") or "").strip()
                column = str(resolved.get("column") or "").strip()
                if table and column:
                    output.append({"table": table, "column": column, "dimension_name": resolved.get("dimension_name")})
                    continue
            normalized = resolve_grain_item(resolved, business_dimensions, time_axis)
            if "." in normalized:
                table, column = split_qualified_ref(normalized)
                if table and column:
                    output.append({"table": table, "column": column})
        return output

    def _normalize_grain(self, items: list[Any], business_dimensions: list[dict], time_axis: dict[str, Any]) -> list[str]:
        output: list[str] = []
        for item in items:
            value = resolve_grain_item(item, business_dimensions, time_axis)
            if value and value not in output:
                output.append(value)
        return output

    def _normalize_tables(
        self,
        raw_tables: list[Any],
        metrics: list[dict[str, Any]],
        filters: list[dict[str, Any]],
        group_by: list[dict[str, Any]],
        grain: list[str],
        time_axis: dict[str, Any],
    ) -> list[str]:
        tables: list[str] = []
        for item in raw_tables:
            if isinstance(item, dict):
                table = str(item.get("table") or item.get("name") or "").strip()
            else:
                table = str(item).strip()
            if table and table not in tables:
                tables.append(table)
        for metric in metrics:
            table = str(metric.get("table") or "").strip()
            if table and table not in tables:
                tables.append(table)
        for flt in filters:
            table = str(flt.get("table") or "").strip()
            if table and table not in tables:
                tables.append(table)
        for group in group_by:
            table = str(group.get("table") or "").strip()
            if table and table not in tables:
                tables.append(table)
        for item in grain:
            if "." in item:
                table, _ = split_qualified_ref(item)
                if table and table not in tables:
                    tables.append(table)
        table = str(time_axis.get("table") or "").strip()
        if table and table not in tables:
            tables.append(table)
        return tables


_SYSTEM = (
    "Voce e o SchemaPlanner do AgenteV2. "
    "Planeje tabelas e relacionamentos sem escrever SQL. "
    "Use somente tabelas e colunas do contexto. Se faltar evidencia, marque open_questions. "
    "Grain deve usar coluna real, e filtros especiais devem usar rule_code/rule_params, nunca SQL bruto. "
    "Saida somente JSON."
)
