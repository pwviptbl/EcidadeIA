from __future__ import annotations

from typing import Any

from agente_v2.contracts.models import SqlArtifact, SqlCriticResult
from agente_v2.infrastructure.logger import log_event


class SqlCritic:
    def run(self, artifact: SqlArtifact, business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlCriticResult:
        errors: list[str] = []
        warnings: list[str] = []
        notes: list[str] = []

        sql = artifact.sql.strip()
        sql_lower = sql.lower()

        if not sql:
            errors.append("sql vazia")
        if not sql_lower.startswith("with") and not sql_lower.startswith("select"):
            errors.append("sql nao e select/with")
        if ";" in sql.rstrip(";"):
            errors.append("sql contem mais de uma instrucao ou ponto e virgula interno")
        for forbidden in (" insert ", " update ", " delete ", " drop ", " alter ", " truncate "):
            if forbidden in f" {sql_lower} ":
                errors.append("sql contem comando nao permitido")
                break

        for table in artifact.tables:
            if table and table.lower() not in sql_lower:
                errors.append(f"sql nao referencia tabela esperada: {table}")

        for join in artifact.joins:
            for left in _as_list(join.get("source_columns") or join.get("left_columns") or join.get("source_column") or join.get("left_column")):
                if left.lower() not in sql_lower:
                    warnings.append(f"sql pode nao estar usando coluna de join esperada: {left}")
            for right in _as_list(join.get("target_columns") or join.get("right_columns") or join.get("target_column") or join.get("right_column")):
                if right.lower() not in sql_lower:
                    warnings.append(f"sql pode nao estar usando coluna de join esperada: {right}")

        for flt in artifact.filters:
            if not isinstance(flt, dict):
                continue
            column = str(flt.get("column") or flt.get("source_column") or "").strip()
            operator = str(flt.get("operator") or "").strip().upper()
            if column and column.split(".")[-1].lower() not in sql_lower:
                warnings.append(f"sql pode nao estar usando coluna de filtro esperada: {column}")
            if operator == "IN" and " in " not in f" {sql_lower} ":
                warnings.append("sql pode nao estar aplicando filtro IN esperado")
            if operator in {"LIKE", "CONTAINS"} and "like" not in sql_lower and "position(" not in sql_lower:
                warnings.append("sql pode nao estar aplicando filtro textual esperado")

        if artifact.operation == "compare_periods":
            time_axis_column = str(artifact.time_axis.get("column") or "").strip()
            if time_axis_column and time_axis_column.lower() not in sql_lower:
                errors.append(f"sql nao referencia a coluna temporal esperada: {time_axis_column}")
            if "filter (where" not in sql_lower and "group by" not in sql_lower:
                warnings.append("compare_periods sem comparacao explicita por periodo")

        if artifact.operation in {"count_by_dimension", "sum_by_dimension"} and artifact.group_by:
            if "group by" not in sql_lower:
                errors.append(f"{artifact.operation} com group_by no plano mas sem GROUP BY na SQL")
            for group in artifact.group_by:
                if isinstance(group, dict):
                    column = str(group.get("column") or "").strip()
                    if column and column.lower() not in sql_lower:
                        warnings.append(f"sql pode nao estar usando coluna de group_by esperada: {column}")

        if len(artifact.joins) > 1 and "distinct" not in sql_lower and artifact.operation != "compare_periods":
            warnings.append("muitos joins sem distinct podem multiplicar linhas; revisar grao")

        notes.append("Critica estatica aplicada sem executar banco.")
        result = SqlCriticResult(ok=not errors, errors=errors, warnings=warnings, notes=notes)
        log_event("sql_critic.done", result.to_dict())
        return result


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
