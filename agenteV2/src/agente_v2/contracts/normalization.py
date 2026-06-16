from __future__ import annotations

import re
from typing import Any


def split_qualified_ref(value: str) -> tuple[str, str]:
    parts = value.strip().split(".")
    if len(parts) < 3:
        return "", value.strip()
    return ".".join(parts[-3:-1]), parts[-1]


def normalize_metric(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {}
    table = str(item.get("table") or item.get("base_table") or item.get("source_table") or "").strip()
    column = str(item.get("column") or item.get("base_column") or item.get("source_column") or "").strip()
    if not table and "." in column:
        table, column = split_qualified_ref(column)
    aggregation = str(item.get("aggregation") or "").strip().upper()
    if aggregation in {"COUNT", "COUNT_DISTINCT"} and column in {"", "1", "*"}:
        column = ""
    metric_name = str(item.get("metric_name") or item.get("name") or "").strip()
    out = {
        "metric_name": metric_name,
        "table": table,
        "column": column,
        "aggregation": aggregation,
    }
    for key in ("description", "rule_code", "rule_params"):
        if item.get(key):
            out[key] = item.get(key)
    return {key: value for key, value in out.items() if value not in ("", None, [], {})}


def normalize_dimension(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {}
    table = str(item.get("table") or item.get("base_table") or item.get("source_table") or "").strip()
    column = str(item.get("column") or item.get("base_column") or item.get("source_column") or "").strip()
    if not table and "." in column:
        table, column = split_qualified_ref(column)
    name = str(item.get("dimension_name") or item.get("name") or "").strip()
    out = {
        "dimension_name": name,
        "table": table,
        "column": column,
    }
    if item.get("description"):
        out["description"] = item.get("description")
    return {key: value for key, value in out.items() if value not in ("", None, [], {})}


def normalize_filter(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {}

    table = str(item.get("table") or item.get("base_table") or item.get("source_table") or "").strip()
    column = str(item.get("column") or item.get("base_column") or item.get("source_column") or "").strip()
    if not table and "." in column:
        table, column = split_qualified_ref(column)

    out: dict[str, Any] = {
        "filter_name": str(item.get("filter_name") or item.get("name") or "").strip(),
        "table": table,
        "column": column,
    }

    if isinstance(item.get("values"), list) and item.get("values"):
        out["operator"] = "IN"
        out["value"] = [str(value) for value in item["values"]]
    elif isinstance(item.get("value"), list) and item.get("value"):
        out["operator"] = "IN"
        out["value"] = item["value"]
    elif item.get("operator") and item.get("value") is not None:
        out["operator"] = str(item.get("operator")).strip().upper()
        out["value"] = item.get("value")
    elif item.get("condition"):
        out.update(_parse_condition(table, column, str(item.get("condition")).strip()))

    if item.get("description"):
        out["description"] = item.get("description")
    if item.get("rule_code"):
        out["rule_code"] = str(item.get("rule_code")).strip()
    if isinstance(item.get("rule_params"), dict) and item.get("rule_params"):
        out["rule_params"] = item.get("rule_params")

    return {key: value for key, value in out.items() if value not in ("", None, [], {})}


def normalize_join(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {}
    source_table = str(item.get("source_table") or item.get("left_table") or "").strip()
    target_table = str(item.get("target_table") or item.get("right_table") or "").strip()
    source_columns = _as_list(item.get("source_columns") or item.get("left_columns") or item.get("source_column") or item.get("left_column"))
    target_columns = _as_list(item.get("target_columns") or item.get("right_columns") or item.get("target_column") or item.get("right_column"))
    join_type = str(item.get("join_type") or item.get("type") or "JOIN").strip().upper()
    join_type = {
        "INNER": "INNER JOIN",
        "LEFT": "LEFT JOIN",
        "RIGHT": "RIGHT JOIN",
        "FULL": "FULL JOIN",
    }.get(join_type, join_type)
    return {
        "source_table": source_table,
        "source_columns": source_columns,
        "target_table": target_table,
        "target_columns": target_columns,
        "join_type": join_type,
    }


def resolve_named_item(item: Any, catalog_items: list[dict[str, Any]], key_name: str) -> Any:
    lookup = {
        str(candidate.get(key_name) or "").strip(): candidate
        for candidate in catalog_items
        if isinstance(candidate, dict) and str(candidate.get(key_name) or "").strip()
    }
    if isinstance(item, str):
        return lookup.get(item, item)
    if isinstance(item, dict):
        key = str(item.get(key_name) or "").strip()
        if key and key in lookup:
            merged = dict(lookup[key])
            merged.update({k: v for k, v in item.items() if v not in ("", None, [], {})})
            return merged
    return item


def resolve_grain_item(item: Any, dimensions: list[dict[str, Any]], time_axis: dict[str, Any]) -> str:
    if isinstance(item, str) and "." in item:
        table, column = split_qualified_ref(item)
        return f"{table}.{column}" if table and column else item
    if isinstance(item, dict):
        table = str(item.get("table") or "").strip()
        column = str(item.get("column") or "").strip()
        if table and column:
            return f"{table}.{column}"
    label = str(item).strip()
    for dimension in dimensions:
        if label == str(dimension.get("dimension_name") or "").strip():
            table = str(dimension.get("table") or "").strip()
            column = str(dimension.get("column") or "").strip()
            if table and column:
                return f"{table}.{column}"
    if label.lower() == "exercicio":
        table = str(time_axis.get("table") or "").strip()
        column = str(time_axis.get("column") or "").strip()
        if table and column:
            return f"{table}.{column}"
    return label


def _parse_condition(table: str, column: str, condition: str) -> dict[str, Any]:
    upper = condition.upper()
    if upper.startswith("LIKE "):
        return {"operator": "LIKE", "value": _unquote(condition[5:].strip())}
    if upper.startswith("ILIKE "):
        return {"operator": "ILIKE", "value": _unquote(condition[6:].strip())}
    if upper.startswith("= "):
        return {"operator": "=", "value": _unquote(condition[2:].strip())}
    if upper.startswith("IN "):
        values = [part.strip().strip("'") for part in condition[3:].strip().strip("()").split(",") if part.strip()]
        return {"operator": "IN", "value": values}
    if condition.upper().startswith("EXISTS ("):
        periods = [int(match) for match in re.findall(r"\b(19\d{2}|20\d{2})\b", condition)]
        period_column_match = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\.(\w+)\s*=\s*(?:19\d{2}|20\d{2})", condition)
        return {
            "rule_code": "common_entities_across_periods",
            "rule_params": {
                "entity_table": table,
                "entity_column": column,
                "period_column": period_column_match[0] if period_column_match else "",
                "periods": periods,
            },
        }
    quoted = re.findall(r"'([^']+)'", condition)
    if "CONT" in upper and quoted:
        return {"operator": "CONTAINS", "value": quoted[0]}
    return {"condition_text": condition}


def _unquote(value: str) -> str:
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
