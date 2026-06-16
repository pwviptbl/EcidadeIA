from __future__ import annotations

from typing import Any

from agente_v2.contracts.models import SqlArtifact
from agente_v2.infrastructure.logger import log_event


class SqlCompiler:
    def run(self, intent_spec: dict[str, Any], business_spec: dict[str, Any], schema_plan: dict[str, Any]) -> SqlArtifact:
        operation = self._resolve_operation(intent_spec, schema_plan)
        if operation == "compare_periods":
            artifact = self._compile_compare_periods(intent_spec, business_spec, schema_plan)
        elif operation == "count_by_dimension":
            artifact = self._compile_count_by_dimension(intent_spec, business_spec, schema_plan)
        elif operation == "sum_by_dimension":
            artifact = self._compile_sum_by_dimension(intent_spec, business_spec, schema_plan)
        else:
            artifact = self._compile_detail_listing(intent_spec, business_spec, schema_plan)
        log_event("sql_compiler.done", artifact.to_dict())
        return artifact

    def _resolve_operation(self, intent_spec: dict[str, Any], schema_plan: dict[str, Any]) -> str:
        intent = str(intent_spec.get("intent") or "").strip()
        if intent in {"compare_periods", "count_by_dimension", "sum_by_dimension", "detail_listing"}:
            return intent
        if len(schema_plan.get("joins") or []):
            return "compare_periods"
        return "detail_listing"

    def _compile_compare_periods(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
    ) -> SqlArtifact:
        year_list = intent_spec.get("years") or self._extract_years(schema_plan)
        if len(year_list) < 2:
            year_list = [2025, 2026]
        years_sql = ", ".join(str(int(year)) for year in year_list[:4])

        filters = _filter_map(business_spec.get("filters") or [])
        only_iptu = _find_only_iptu_filter(filters)

        sql = f"""
WITH calculo_base AS (
  SELECT
    c.j21_anousu,
    c.j21_matric,
    c.j21_codhis,
    c.j21_valor,
    p.j23_arealo,
    p.j23_m2terr,
    p.j23_areaed,
    p.j23_areafr,
    p.j23_aliq,
    p.j23_vlrter,
    p.j23_vlrisen,
    p.j23_testad
  FROM cadastro.iptucalv c
  JOIN cadastro.iptucalc p
    ON p.j23_matric = c.j21_matric
   AND p.j23_anousu = c.j21_anousu
  JOIN cadastro.iptucalh h
    ON h.j17_codhis = c.j21_codhis
  WHERE c.j21_anousu IN ({years_sql})
    AND {only_iptu}
)
SELECT
  c.j21_anousu AS exercicio,
  SUM(c.j21_valor) AS valor_total_iptu,
  SUM(c.j23_arealo) AS area_total_lote_calculada,
  AVG(c.j23_m2terr) AS valor_m2_terreno,
  SUM(c.j23_areaed) AS area_total_edificada_calculada,
  SUM(c.j23_areafr) AS area_fracionada_calculada,
  AVG(c.j23_aliq) AS aliquota_aplicada,
  SUM(c.j23_vlrter) AS valor_venal_terreno,
  SUM(c.j23_vlrisen) AS valor_isencao,
  AVG(c.j23_testad) AS testada_media
FROM calculo_base c
GROUP BY c.j21_anousu
ORDER BY c.j21_anousu
""".strip()
        return SqlArtifact(
            operation="compare_periods",
            sql=sql,
            limit=1000,
            tables=["cadastro.iptucalv", "cadastro.iptucalc", "cadastro.iptucalh"],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=business_spec.get("metrics") or [],
            group_by=schema_plan.get("group_by") or [],
            notes=[
                "SQL compilado a partir de plano validado.",
                "Filtro de IPTU aplicado via historico.",
            ],
        )

    def _compile_count_by_dimension(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
    ) -> SqlArtifact:
        return self._compile_passthrough("count_by_dimension", schema_plan, business_spec)

    def _compile_sum_by_dimension(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
    ) -> SqlArtifact:
        return self._compile_passthrough("sum_by_dimension", schema_plan, business_spec)

    def _compile_detail_listing(
        self,
        intent_spec: dict[str, Any],
        business_spec: dict[str, Any],
        schema_plan: dict[str, Any],
    ) -> SqlArtifact:
        return self._compile_passthrough("detail_listing", schema_plan, business_spec)

    def _compile_passthrough(self, operation: str, schema_plan: dict[str, Any], business_spec: dict[str, Any]) -> SqlArtifact:
        sql = "-- operacao ainda nao implementada para este plano"
        return SqlArtifact(
            operation=operation,
            sql=sql,
            limit=1000,
            tables=schema_plan.get("tables") or [],
            joins=schema_plan.get("joins") or [],
            filters=schema_plan.get("filters") or [],
            metrics=business_spec.get("metrics") or [],
            group_by=schema_plan.get("group_by") or [],
            notes=["Operacao generica ainda nao expandida."],
        )

    def _extract_years(self, schema_plan: dict[str, Any]) -> list[int]:
        years: list[int] = []
        for item in schema_plan.get("filters") or []:
            value = item.get("value") if isinstance(item, dict) else None
            if isinstance(value, list):
                years.extend(int(v) for v in value if str(v).isdigit())
        return sorted(set(years))


def _normalized_column(metric: dict[str, Any]) -> str:
    column = str(metric.get("column") or metric.get("base_column") or metric.get("source_column") or "").strip()
    return column


def _metric_map(metrics: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for metric in metrics:
        if isinstance(metric, dict):
            name = str(metric.get("metric_name") or metric.get("name") or "").strip()
            if name:
                result[name] = metric
    return result


def _filter_map(filters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for flt in filters:
        if isinstance(flt, dict):
            name = str(flt.get("filter_name") or flt.get("name") or "").strip()
            if name:
                result[name] = flt
    return result


def _find_only_iptu_filter(filters: dict[str, dict[str, Any]]) -> str:
    for key in ("Somente IPTU", "Somente_IPTU_Historico", "somente_iptu"):
        flt = filters.get(key)
        if flt:
            return f"position('iptu' in lower(h.j17_descr)) > 0"
    return "position('iptu' in lower(h.j17_descr)) > 0"
