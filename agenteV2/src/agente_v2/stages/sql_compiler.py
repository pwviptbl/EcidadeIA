from __future__ import annotations

import unicodedata
from typing import Any

from agente_v2.contracts.models import SqlArtifact
from agente_v2.contracts.normalization import resolve_grain_item
from agente_v2.infrastructure.logger import log_event


class SqlCompiler:
    def run(self, intent_spec: dict[str, Any], business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlArtifact:
        operation = self._resolve_operation(intent_spec)
        if operation == "compare_periods":
            artifact = self._compile_compare_periods(intent_spec, business_spec, schema_plan)
        elif operation == "count_by_dimension":
            artifact = self._compile_count_by_dimension(business_spec, schema_plan)
        elif operation == "sum_by_dimension":
            artifact = self._compile_sum_by_dimension(business_spec, schema_plan)
        else:
            artifact = self._compile_detail_listing(business_spec, schema_plan)
        log_event("sql_compiler.done", artifact.to_dict())
        return artifact

    def _resolve_operation(self, intent_spec: dict[str, Any]) -> str:
        intent = str(intent_spec.get("intent") or "").strip()
        if intent in {"compare_periods", "count_by_dimension", "sum_by_dimension", "detail_listing"}:
            return intent
        return "detail_listing"

    def _compile_compare_periods(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
    ) -> SqlArtifact:
        years = _extract_years(intent_spec, schema_plan)
        base = _base_query(schema_plan, business_spec)
        time_axis = _time_axis(schema_plan)
        year_expr = _base_column_expr(time_axis["table"], time_axis["column"], base["selected"])
        metric_selects = []
        for metric in _resolved_metrics(business_spec, schema_plan):
            agg = _sql_agg(metric)
            expr = _base_column_expr(_metric_table(metric, schema_plan), _metric_column(metric), base["selected"])
            alias = _metric_alias(metric)
            metric_selects.append(
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[0]}) AS {alias}_{years[0]},\n"
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[1]}) AS {alias}_{years[1]},\n"
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[1]}) - {agg}({expr}) FILTER (WHERE {year_expr} = {years[0]}) AS delta_{alias}"
            )
        sql = (
            f"WITH base AS (\n{base['sql']}\n)\n"
            "SELECT\n"
            + ",\n".join(metric_selects)
            + "\nFROM base b"
        )
        return SqlArtifact(
            operation="compare_periods",
            sql=sql,
            limit=1000,
            tables=schema_plan.get("tables") or [],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=_resolved_metrics(business_spec, schema_plan),
            group_by=schema_plan.get("group_by") or [],
            time_axis=time_axis,
            notes=["SQL compilado genericamente a partir do plano validado."],
        )

    def _compile_count_by_dimension(self, business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlArtifact:
        metric = _resolved_metrics(business_spec, schema_plan)[0]
        table = _metric_table(metric, schema_plan)
        column = _metric_column(metric)
        alias = _metric_alias(metric)
        group_by = _normalize_group_by(schema_plan.get("group_by") or [], business_spec, schema_plan)
        if group_by:
            sql = _compile_grouped_aggregation(
                group_by=group_by,
                schema_plan=schema_plan,
                metric=metric,
                aggregate_alias=alias,
            )
        else:
            sql = _compile_direct_aggregation(
                schema_plan=schema_plan,
                metric=metric,
                aggregate_alias=alias,
            )
        return SqlArtifact(
            operation="count_by_dimension",
            sql=sql,
            limit=1000,
            tables=[table] if table else [],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=[metric],
            group_by=schema_plan.get("group_by") or [],
            time_axis=schema_plan.get("time_axis") if isinstance(schema_plan.get("time_axis"), dict) else {},
            notes=["Contagem compilada genericamente a partir da metrica validada."],
        )

    def _compile_sum_by_dimension(self, business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlArtifact:
        metric = _resolved_metrics(business_spec, schema_plan)[0]
        table = _metric_table(metric, schema_plan)
        column = _metric_column(metric)
        alias = _metric_alias(metric)
        group_by = _normalize_group_by(schema_plan.get("group_by") or [], business_spec, schema_plan)
        if group_by:
            sql = _compile_grouped_aggregation(
                group_by=group_by,
                schema_plan=schema_plan,
                metric=metric,
                aggregate_alias=alias,
            )
        else:
            sql = _compile_direct_aggregation(
                schema_plan=schema_plan,
                metric=metric,
                aggregate_alias=alias,
            )
        return SqlArtifact(
            operation="sum_by_dimension",
            sql=sql,
            limit=1000,
            tables=[table] if table else [],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=[metric],
            group_by=schema_plan.get("group_by") or [],
            time_axis=schema_plan.get("time_axis") if isinstance(schema_plan.get("time_axis"), dict) else {},
            notes=["Soma compilada genericamente a partir da metrica validada."],
        )

    def _compile_detail_listing(self, business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlArtifact:
        table = str((schema_plan.get("tables") or [""])[0]).strip()
        sql = f"SELECT *\nFROM {table}\nLIMIT 1000"
        return SqlArtifact(
            operation="detail_listing",
            sql=sql,
            limit=1000,
            tables=[table] if table else [],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=_resolved_metrics(business_spec, schema_plan),
            group_by=schema_plan.get("group_by") or [],
            time_axis=schema_plan.get("time_axis") if isinstance(schema_plan.get("time_axis"), dict) else {},
            notes=["Listagem compilada genericamente a partir do plano validado."],
        )


def _base_query(schema_plan: dict[str, Any], business_spec: dict[str, Any]) -> dict[str, Any]:
    tables = [str(item).strip() for item in (schema_plan.get("tables") or []) if str(item).strip()]
    aliases = {table: f"t{index + 1}" for index, table in enumerate(tables)}
    select_columns: list[str] = []
    seen: set[str] = set()
    selected: dict[tuple[str, str], str] = {}

    time_axis = _time_axis_optional(schema_plan)
    if time_axis:
        _collect_column(select_columns, seen, selected, time_axis["table"], time_axis["column"], aliases)

    for metric in _resolved_metrics(business_spec, schema_plan):
        table = _metric_table(metric, schema_plan)
        column = _metric_column(metric)
        if table and column:
            _collect_column(select_columns, seen, selected, table, column, aliases)

    for item in schema_plan.get("filters") or []:
        if isinstance(item, dict):
            table = str(item.get("table") or item.get("source_table") or "").strip()
            column = str(item.get("column") or item.get("source_column") or "").strip()
            if table and column:
                _collect_column(select_columns, seen, selected, table, column, aliases)

    for grain in _normalize_grain(schema_plan.get("grain") or [], business_spec, schema_plan):
        if isinstance(grain, str) and "." in grain:
            table, column = _split_column_ref(grain)
            if table and column:
                _collect_column(select_columns, seen, selected, table, column, aliases)

    for group in _normalize_group_by(schema_plan.get("group_by") or [], business_spec, schema_plan):
        table = str(group.get("table") or "").strip()
        column = str(group.get("column") or "").strip()
        if table and column:
            _collect_column(select_columns, seen, selected, table, column, aliases)

    joins = _merge_joins(schema_plan.get("joins") or [])
    first_table = tables[0]
    lines = ["  SELECT", "    " + ",\n    ".join(select_columns), f"  FROM {first_table} {aliases[first_table]}"]
    for join in joins:
        left_table = str(join.get("source_table") or join.get("left_table") or "").strip()
        right_table = str(join.get("target_table") or join.get("right_table") or "").strip()
        left_columns = _as_list(join.get("source_columns") or join.get("left_columns") or join.get("source_column") or join.get("left_column"))
        right_columns = _as_list(join.get("target_columns") or join.get("right_columns") or join.get("target_column") or join.get("right_column"))
        join_type = _normalize_join_type(join)
        on_parts = []
        for left, right in zip(left_columns, right_columns):
            on_parts.append(f"{aliases[left_table]}.{left} = {aliases[right_table]}.{right}")
        lines.append(f"  {join_type} {right_table} {aliases[right_table]}")
        lines.append(f"    ON {' AND '.join(on_parts)}")

    where_parts = _compile_filters(schema_plan.get("filters") or [], aliases)
    if where_parts:
        lines.append("  WHERE " + "\n    AND ".join(where_parts))
    return {"sql": "\n".join(lines), "aliases": aliases, "selected": selected}


def _compile_filters(filters: list[Any], aliases: dict[str, str]) -> list[str]:
    where_parts: list[str] = []
    for item in filters:
        if not isinstance(item, dict):
            continue
        table = str(item.get("table") or item.get("source_table") or "").strip()
        column = str(item.get("column") or item.get("source_column") or "").strip()
        operator = str(item.get("operator") or "").strip().upper()
        value = item.get("value")
        rule_code = str(item.get("rule_code") or "").strip()
        rule_params = item.get("rule_params") if isinstance(item.get("rule_params"), dict) else {}
        if table and column:
            expr = _column_expr(table, column, aliases)
        else:
            expr = ""
        if not table or not column or not operator:
            if rule_code == "common_entities_across_periods" and table and column:
                where_parts.append(_compile_rule_common_entities(expr, aliases, rule_params))
                continue
            if not table or not column:
                continue
        if operator == "IN" and isinstance(value, list):
            values_sql = ", ".join(_sql_literal(v) for v in value)
            where_parts.append(f"{expr} IN ({values_sql})")
        elif operator in {"LIKE", "ILIKE", "CONTAINS"}:
            if operator == "CONTAINS":
                where_parts.append(f"position(lower({_sql_literal(str(value))}) in lower({expr})) > 0")
            else:
                where_parts.append(f"{expr} {operator} {_sql_literal(value)}")
        elif operator in {"=", "EQ"}:
            where_parts.append(f"{expr} = {_sql_literal(value)}")
    return where_parts


def _resolved_metrics(business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> list[dict[str, Any]]:
    business_metrics = business_spec.get("metrics") or []
    if not schema_plan.get("metrics"):
        return [metric for metric in business_metrics if isinstance(metric, dict)]
    result: list[dict[str, Any]] = []
    by_name = {
        str(item.get("metric_name") or item.get("name") or "").strip(): item
        for item in business_metrics
        if isinstance(item, dict)
    }
    for item in schema_plan.get("metrics") or []:
        if isinstance(item, dict):
            result.append(item)
        elif isinstance(item, str) and item in by_name:
            result.append(by_name[item])
    return result or [metric for metric in business_metrics if isinstance(metric, dict)]


def _metric_table(metric: dict[str, Any], schema_plan: dict[str, Any]) -> str:
    table = str(metric.get("table") or metric.get("base_table") or metric.get("source_table") or "").strip()
    if table:
        return table
    raw_column = str(metric.get("column") or metric.get("base_column") or metric.get("source_column") or "").strip()
    if "." in raw_column:
        table, _ = _split_column_ref(raw_column)
        return table
    return str((schema_plan.get("tables") or [""])[0]).strip()


def _metric_column(metric: dict[str, Any]) -> str:
    value = str(metric.get("column") or metric.get("base_column") or metric.get("source_column") or "").strip()
    if "." in value:
        _, column = _split_column_ref(value)
        return column
    return value


def _time_axis(schema_plan: dict[str, Any]) -> dict[str, str]:
    time_axis = schema_plan.get("time_axis")
    if isinstance(time_axis, dict):
        table = str(time_axis.get("table") or "").strip()
        column = str(time_axis.get("column") or "").strip()
        if table and column:
            return {"table": table, "column": column}
    raise ValueError("compare_periods exige time_axis estruturado no schema_plan")


def _time_axis_optional(schema_plan: dict[str, Any]) -> dict[str, str]:
    try:
        return _time_axis(schema_plan)
    except ValueError:
        return {}


def _column_expr(table: str, column: str, aliases: dict[str, str]) -> str:
    return f"{aliases[table]}.{column}"


def _split_column_ref(value: str) -> tuple[str, str]:
    parts = value.strip().split(".")
    if len(parts) < 3:
        return "", value.strip()
    return ".".join(parts[-3:-1]), parts[-1]


def _collect_column(
    select_columns: list[str],
    seen: set[str],
    selected: dict[tuple[str, str], str],
    table: str,
    column: str,
    aliases: dict[str, str],
) -> None:
    expr = _column_expr(table, column, aliases)
    alias = _selected_alias(table, column)
    if expr not in seen:
        select_columns.append(f"{expr} AS {alias}")
        seen.add(expr)
    selected[(table, column)] = alias


def _selected_alias(table: str, column: str) -> str:
    safe_table = table.replace(".", "__")
    return f"{safe_table}__{column}"


def _base_column_expr(table: str, column: str, selected: dict[tuple[str, str], str]) -> str:
    return f"b.{selected[(table, column)]}"


def _compile_rule_common_entities(expr: str, aliases: dict[str, str], rule_params: dict[str, Any]) -> str:
    entity_table = str(rule_params.get("entity_table") or "").strip()
    entity_column = str(rule_params.get("entity_column") or "").strip()
    period_column = str(rule_params.get("period_column") or "").strip()
    periods = [int(item) for item in (rule_params.get("periods") or []) if str(item).isdigit()]
    if not entity_table or not entity_column or not period_column or len(periods) < 2:
        return "1 = 1"
    alias = aliases.get(entity_table, "")
    if not alias:
        return "1 = 1"
    parts = [
        f"EXISTS (SELECT 1 FROM {entity_table} AS p{index + 1} WHERE p{index + 1}.{entity_column} = {expr} AND p{index + 1}.{period_column} = {period})"
        for index, period in enumerate(periods)
    ]
    return " AND ".join(parts)


def _normalize_group_by(items: list[Any], business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> list[dict[str, Any]]:
    dimensions = [item for item in (business_spec.get("dimensions") or []) if isinstance(item, dict)]
    time_axis = schema_plan.get("time_axis") if isinstance(schema_plan.get("time_axis"), dict) else {}
    result: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            table = str(item.get("table") or "").strip()
            column = str(item.get("column") or "").strip()
            if not table and "." in column:
                table, column = _split_column_ref(column)
            if table and column:
                result.append({"table": table, "column": column})
                continue
        if isinstance(item, str):
            for dimension in dimensions:
                if item == str(dimension.get("dimension_name") or "").strip():
                    table = str(dimension.get("table") or "").strip()
                    column = str(dimension.get("column") or "").strip()
                    if table and column:
                        result.append({"table": table, "column": column})
                        break
            else:
                if item.lower() == "exercicio":
                    table = str(time_axis.get("table") or "").strip()
                    column = str(time_axis.get("column") or "").strip()
                    if table and column:
                        result.append({"table": table, "column": column})
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in result:
        key = (item["table"], item["column"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def _normalize_grain(items: list[Any], business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> list[str]:
    dimensions = [item for item in (business_spec.get("dimensions") or []) if isinstance(item, dict)]
    time_axis = schema_plan.get("time_axis") if isinstance(schema_plan.get("time_axis"), dict) else {}
    output: list[str] = []
    for item in items:
        resolved = resolve_grain_item(item, dimensions, time_axis)
        if resolved and resolved not in output:
            output.append(resolved)
    return output


def _merge_joins(joins: list[Any]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str, str], dict[str, Any]] = {}
    ordered: list[tuple[str, str, str]] = []
    for item in joins:
        if not isinstance(item, dict):
            continue
        source_table = str(item.get("source_table") or item.get("left_table") or "").strip()
        target_table = str(item.get("target_table") or item.get("right_table") or "").strip()
        join_type = _normalize_join_type(item)
        key = (source_table, target_table, join_type)
        if key not in merged:
            merged[key] = {
                "source_table": source_table,
                "target_table": target_table,
                "join_type": join_type,
                "source_columns": [],
                "target_columns": [],
            }
            ordered.append(key)
        merged[key]["source_columns"].extend(_as_list(item.get("source_columns") or item.get("left_columns") or item.get("source_column") or item.get("left_column")))
        merged[key]["target_columns"].extend(_as_list(item.get("target_columns") or item.get("right_columns") or item.get("target_column") or item.get("right_column")))
    return [merged[key] for key in ordered]


def _sql_agg(metric: dict[str, Any]) -> str:
    agg = str(metric.get("aggregation") or "SUM").strip().upper()
    return {
        "COUNT_DISTINCT": "COUNT",
        "COUNT": "COUNT",
        "SUM": "SUM",
        "AVG": "AVG",
        "MAX": "MAX",
        "MIN": "MIN",
    }.get(agg, agg)


def _normalize_join_type(item: dict[str, Any]) -> str:
    join_type = str(item.get("join_type") or item.get("type") or "JOIN").strip().upper()
    return {
        "INNER": "INNER JOIN",
        "LEFT": "LEFT JOIN",
        "RIGHT": "RIGHT JOIN",
        "FULL": "FULL JOIN",
    }.get(join_type, join_type)


def _column_ref(table: str, column: str) -> str:
    return f"{table}.{column}" if table and column else column


def _aggregation_expression(metric: dict[str, Any], column_ref: str) -> str:
    agg = str(metric.get("aggregation") or "SUM").strip().upper()
    if agg == "COUNT_DISTINCT" and column_ref:
        return f"COUNT(DISTINCT {column_ref})"
    if agg == "COUNT" and column_ref:
        return f"COUNT({column_ref})"
    if agg == "COUNT":
        return "COUNT(1)"
    return f"{_sql_agg(metric)}({column_ref})" if column_ref else f"{_sql_agg(metric)}(1)"


def _compile_grouped_aggregation(
    group_by: list[dict[str, Any]],
    schema_plan: dict[str, Any],
    metric: dict[str, Any],
    aggregate_alias: str,
) -> str:
    tables = [str(item).strip() for item in (schema_plan.get("tables") or []) if str(item).strip()]
    aliases = {table: f"t{index + 1}" for index, table in enumerate(tables)}
    if not tables:
        raise ValueError("schema_plan exige tables para agregacao agrupada")

    select_parts = [
        f"  {aliases[item['table']]}.{item['column']} AS {_selected_alias(item['table'], item['column'])}"
        for item in group_by
    ]
    table = _metric_table(metric, schema_plan)
    column = _metric_column(metric)
    select_parts.append(f"  {_aggregation_expression(metric, _column_ref(aliases.get(table, table), column))} AS {aggregate_alias}")

    lines = [
        "SELECT",
        ",\n".join(select_parts),
        f"FROM {tables[0]} {aliases[tables[0]]}",
    ]

    for join in _merge_joins(schema_plan.get("joins") or []):
        left_table = str(join.get("source_table") or join.get("left_table") or "").strip()
        right_table = str(join.get("target_table") or join.get("right_table") or "").strip()
        left_columns = _as_list(join.get("source_columns") or join.get("left_columns") or join.get("source_column") or join.get("left_column"))
        right_columns = _as_list(join.get("target_columns") or join.get("right_columns") or join.get("target_column") or join.get("right_column"))
        join_type = _normalize_join_type(join)
        on_parts = []
        for left, right in zip(left_columns, right_columns):
            on_parts.append(f"{aliases[left_table]}.{left} = {aliases[right_table]}.{right}")
        lines.append(f"{join_type} {right_table} {aliases[right_table]}")
        lines.append(f"  ON {' AND '.join(on_parts)}")

    where_parts = _compile_filters(schema_plan.get("filters") or [], aliases)
    if where_parts:
        lines.append("WHERE " + "\n  AND ".join(where_parts))

    group_cols = ", ".join(f"{aliases[item['table']]}.{item['column']}" for item in group_by)
    order_cols = ", ".join(f"{aliases[item['table']]}.{item['column']}" for item in group_by)
    if group_cols:
        lines.append(f"GROUP BY {group_cols}")
    if order_cols:
        lines.append(f"ORDER BY {order_cols}")
    return "\n".join(lines)


def _compile_direct_aggregation(schema_plan: dict[str, Any], metric: dict[str, Any], aggregate_alias: str) -> str:
    tables = [str(item).strip() for item in (schema_plan.get("tables") or []) if str(item).strip()]
    aliases = {table: f"t{index + 1}" for index, table in enumerate(tables)}
    if not tables:
        raise ValueError("schema_plan exige tables para agregacao direta")

    table = _metric_table(metric, schema_plan)
    column = _metric_column(metric)
    table_alias = aliases.get(table, aliases[tables[0]])
    select_expr = _aggregation_expression(metric, f"{table_alias}.{column}")
    lines = [
        "SELECT",
        f"  {select_expr} AS {aggregate_alias}",
        f"FROM {tables[0]} {aliases[tables[0]]}",
    ]

    for join in _merge_joins(schema_plan.get("joins") or []):
        left_table = str(join.get("source_table") or join.get("left_table") or "").strip()
        right_table = str(join.get("target_table") or join.get("right_table") or "").strip()
        left_columns = _as_list(join.get("source_columns") or join.get("left_columns") or join.get("source_column") or join.get("left_column"))
        right_columns = _as_list(join.get("target_columns") or join.get("right_columns") or join.get("target_column") or join.get("right_column"))
        join_type = _normalize_join_type(join)
        on_parts = []
        for left, right in zip(left_columns, right_columns):
            on_parts.append(f"{aliases[left_table]}.{left} = {aliases[right_table]}.{right}")
        lines.append(f"{join_type} {right_table} {aliases[right_table]}")
        lines.append(f"  ON {' AND '.join(on_parts)}")

    where_parts = _compile_filters(schema_plan.get("filters") or [], aliases)
    if where_parts:
        lines.append("WHERE " + "\n  AND ".join(where_parts))
    return "\n".join(lines)


def _metric_alias(metric: dict[str, Any]) -> str:
    name = str(metric.get("metric_name") or metric.get("name") or "metric").strip().lower()
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    out = []
    prev_sep = False
    for char in name:
        if char.isalnum():
            out.append(char)
            prev_sep = False
        else:
            if not prev_sep:
                out.append("_")
                prev_sep = True
    return "".join(out).strip("_") or "metric"


def _extract_years(intent_spec: dict[str, Any], schema_plan: dict[str, Any]) -> list[int]:
    years = [int(year) for year in (intent_spec.get("years") or []) if str(year).isdigit()]
    if len(years) >= 2:
        return years[:2]
    for item in schema_plan.get("filters") or []:
        if isinstance(item, dict) and isinstance(item.get("value"), list):
            values = [int(v) for v in item.get("value") if str(v).isdigit()]
            if len(values) >= 2:
                return values[:2]
    raise ValueError("compare_periods exige dois periodos numericos")


def _sql_literal(value: Any) -> str:
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("'", "''")
    return f"'{text}'"


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
