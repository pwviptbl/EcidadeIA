from __future__ import annotations

from typing import Any

from agente_v2.contracts.models import StageResult
from agente_v2.infrastructure.logger import log_event


class PlanValidator:
    def run(self, schema_plan: dict[str, Any], business_spec: dict[str, Any], context: dict[str, Any]) -> StageResult:
        errors: list[str] = []
        warnings: list[str] = []
        known_tables = set(context.get("described_tables") or {})
        known_columns = {
            table: set(_columns_from_describe(payload))
            for table, payload in (context.get("described_tables") or {}).items()
        }

        for table in schema_plan.get("tables") or []:
            table_name = str(table)
            if table_name not in known_tables:
                errors.append(f"tabela fora do contexto ou nao descrita: {table_name}")

        if not schema_plan.get("entity"):
            errors.append("entity ausente no schema_plan")
        if not schema_plan.get("grain"):
            errors.append("grain ausente no schema_plan")

        time_axis = schema_plan.get("time_axis") or {}
        requires_time_axis = str((schema_plan.get("time_axis") or {}).get("column") or "").strip() or any(
            str(item.get("value") or "").strip() for item in (schema_plan.get("filters") or []) if isinstance(item, dict)
        )
        if time_axis:
            self._validate_column_ref(time_axis, known_columns, errors, "time_axis")
        elif requires_time_axis:
            warnings.append("time_axis nao informado")

        metrics = _resolve_named_items(schema_plan.get("metrics") or [], business_spec.get("metrics") or [], "metric_name")
        filters = _resolve_named_items(schema_plan.get("filters") or [], business_spec.get("filters") or [], "filter_name")

        for index, metric in enumerate(metrics):
            if isinstance(metric, dict) and str(metric.get("aggregation") or "").upper() in {"COUNT", "COUNT_DISTINCT"}:
                self._validate_count_metric(metric, known_columns, errors, f"metric[{index}]")
            else:
                self._validate_column_ref(metric, known_columns, errors, f"metric[{index}]")
            if isinstance(metric, dict) and not metric.get("aggregation"):
                warnings.append(f"metric[{index}] sem aggregation")

        group_by = _resolve_named_items(schema_plan.get("group_by") or [], business_spec.get("dimensions") or [], "dimension_name")

        for index, group in enumerate(group_by):
            self._validate_column_ref(group, known_columns, errors, f"group_by[{index}]")

        for index, flt in enumerate(filters):
            if isinstance(flt, dict):
                self._validate_column_ref(flt, known_columns, errors, f"filter[{index}]")
            else:
                warnings.append(f"filter[{index}] sem definicao estruturada: {flt}")

        joins = schema_plan.get("joins") or []
        if len(schema_plan.get("tables") or []) > 1 and not joins:
            errors.append("plano usa multiplas tabelas sem joins explicitos")
        for index, join in enumerate(joins):
            self._validate_join(join, known_columns, errors, f"join[{index}]")

        if not (business_spec.get("evidence") or business_spec.get("resolved_terms")):
            warnings.append("business_spec sem evidencia/resolucao explicita")
        if not (metrics or group_by):
            warnings.append("schema_plan sem metricas ou agrupamentos")

        payload = {
            "ok": not errors,
            "errors": errors,
            "warnings": warnings,
            "known_tables": sorted(known_tables),
        }
        log_event("plan_validator.done", payload)
        return StageResult("PlanValidator", payload, errors)

    def _validate_column_ref(self, item: Any, known_columns: dict[str, set[str]], errors: list[str], label: str) -> None:
        table = ""
        column = ""
        if isinstance(item, str):
            table, column = _split_column_ref(item)
        elif isinstance(item, dict):
            table = str(item.get("table") or item.get("source_table") or item.get("base_table") or "").strip()
            column = str(item.get("column") or item.get("source_column") or item.get("base_column") or item.get("expression") or "").strip()
            if not table and "." in column:
                table, column = _split_column_ref(column)
        else:
            errors.append(f"{label} em formato invalido")
            return
        if not table or not column:
            errors.append(f"{label} sem table/column")
            return
        if table not in known_columns:
            errors.append(f"{label}.table fora do contexto: {table}")
            return
        if column and column not in known_columns.get(table, set()):
            errors.append(f"{label}.column fora do catalogo de {table}: {column}")

    def _validate_join(self, join: dict, known_columns: dict[str, set[str]], errors: list[str], label: str) -> None:
        left_table = str(join.get("left_table") or join.get("source_table") or "").strip()
        right_table = str(join.get("right_table") or join.get("target_table") or "").strip()
        left_columns = _as_list(join.get("left_columns") or join.get("source_columns") or join.get("left_column") or join.get("source_column"))
        right_columns = _as_list(join.get("right_columns") or join.get("target_columns") or join.get("right_column") or join.get("target_column"))
        if not all([left_table, right_table, left_columns, right_columns]):
            errors.append(f"{label} incompleto")
            return
        if len(left_columns) != len(right_columns):
            errors.append(f"{label} com quantidade diferente de colunas")
            return
        for column in left_columns:
            self._validate_join_column(left_table, column, known_columns, errors, label, "left")
        for column in right_columns:
            self._validate_join_column(right_table, column, known_columns, errors, label, "right")

    def _validate_join_column(
        self,
        table: str,
        column: str,
        known_columns: dict[str, set[str]],
        errors: list[str],
        label: str,
        side: str,
    ) -> None:
        if table not in known_columns:
            errors.append(f"{label}.{side}_table fora do contexto: {table}")
        elif column not in known_columns[table]:
            errors.append(f"{label}.{side}_column fora do catalogo de {table}: {column}")

    def _validate_count_metric(self, item: dict[str, Any], known_columns: dict[str, set[str]], errors: list[str], label: str) -> None:
        table = str(item.get("table") or item.get("base_table") or item.get("source_table") or "").strip()
        column = str(item.get("column") or item.get("base_column") or item.get("source_column") or "").strip()
        if not table:
            errors.append(f"{label} sem table")
            return
        if table not in known_columns:
            errors.append(f"{label}.table fora do contexto: {table}")
            return
        if column and column not in {"1", "*"} and column not in known_columns.get(table, set()):
            errors.append(f"{label}.column fora do catalogo de {table}: {column}")


def _columns_from_describe(payload: dict) -> list[str]:
    catalog = payload.get("catalog") if isinstance(payload.get("catalog"), dict) else {}
    columns = payload.get("columns") or catalog.get("columns") or catalog.get("colunas") or []
    if isinstance(columns, dict):
        return list(columns.keys())
    if isinstance(columns, list):
        result = []
        for item in columns:
            if isinstance(item, dict):
                result.append(str(item.get("name") or item.get("column") or item.get("column_name") or ""))
            else:
                result.append(str(item))
        return [item for item in result if item]
    return []


def _split_column_ref(value: str) -> tuple[str, str]:
    parts = value.strip().split(".")
    if len(parts) < 3:
        return "", value.strip()
    return ".".join(parts[-3:-1]), parts[-1]


def _resolve_named_items(items: list[Any], catalog_items: list[Any], name_key: str) -> list[Any]:
    by_name = {
        str(item.get(name_key) or ""): item
        for item in catalog_items
        if isinstance(item, dict) and item.get(name_key)
    }
    resolved: list[Any] = []
    for item in items:
        if isinstance(item, str) and item in by_name:
            resolved.append(by_name[item])
        else:
            resolved.append(item)
    return resolved


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
