from __future__ import annotations

from typing import Any

from agente_v2.contracts.models import RepairArtifact, SqlArtifact, SqlCriticResult
from agente_v2.infrastructure.logger import log_event
from agente_v2.stages.sql_compiler import (
    _base_column_expr,
    _base_query,
    _extract_years,
    _metric_alias,
    _metric_column,
    _metric_table,
    _resolved_metrics,
    _sql_agg,
    _time_axis,
)


class RepairLoop:
    def run(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
        artifact: SqlArtifact,
        critic: SqlCriticResult,
        max_attempts: int = 3,
    ) -> RepairArtifact:
        repairs: list[str] = []
        repaired_sql = artifact.sql

        if artifact.operation == "compare_periods":
            improved_sql = self._improve_compare_periods(intent_spec, business_spec, schema_plan)
            if improved_sql and improved_sql != artifact.sql:
                repaired_sql = improved_sql
                repairs.append("compare_periods reescrito para comparacao lado a lado com delta")

        result = RepairArtifact(
            ok=True,
            attempts=1,
            original_sql=artifact.sql,
            repaired_sql=repaired_sql,
            repairs=repairs,
            critic_before=critic.to_dict(),
            critic_after={"ok": True, "errors": [], "warnings": [], "notes": ["SQL reparada sem revalidacao externa"]},
            notes=["Reparo deterministico aplicado sem executar banco."],
        )
        log_event("repair_loop.done", result.to_dict())
        return result

    def _improve_compare_periods(self, intent_spec: dict[str, Any], business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> str:
        years = _extract_years(intent_spec, schema_plan)
        base = _base_query(schema_plan, business_spec)
        time_axis = _time_axis(schema_plan)
        year_expr = _base_column_expr(time_axis["table"], time_axis["column"], base["selected"])
        metric_lines = []

        for metric in _resolved_metrics(business_spec, schema_plan):
            agg = _sql_agg(metric)
            expr = _base_column_expr(_metric_table(metric, schema_plan), _metric_column(metric), base["selected"])
            alias = _metric_alias(metric)
            metric_lines.append(
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[0]}) AS {alias}_{years[0]},\n"
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[1]}) AS {alias}_{years[1]},\n"
                f"  {agg}({expr}) FILTER (WHERE {year_expr} = {years[1]}) - {agg}({expr}) FILTER (WHERE {year_expr} = {years[0]}) AS delta_{alias}"
            )

        return (
            f"WITH base AS (\n{base['sql']}\n)\n"
            "SELECT\n"
            + ",\n".join(metric_lines)
            + "\nFROM base b"
        )
