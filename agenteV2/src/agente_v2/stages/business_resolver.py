from __future__ import annotations

from typing import Any

from agente_v2.context import compact_context
from agente_v2.contracts.normalization import normalize_dimension, normalize_filter, normalize_metric
from agente_v2.contracts.models import IntentSpec, StageResult
from agente_v2.infrastructure.llm import LLMClient, LLMError
from agente_v2.infrastructure.logger import log_event


class BusinessResolver:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, question: str, intent: IntentSpec, context: dict[str, Any]) -> StageResult:
        payload = {
            "task": (
                "Resolva termos humanos usando somente as evidencias de negocio do contexto. "
                "Nao gere SQL. Retorne regras, metricas, filtros e riscos em JSON. "
                "Filtros devem ser estruturados com operator/value ou rule_code/rule_params. "
                "Nao use condition com SQL bruto."
            ),
            "question": question,
            "intent_spec": intent.to_dict(),
            "context": compact_context(context),
            "response_schema": {
                "resolved_terms": [],
                "metrics": [],
                "filters": [],
                "dimensions": [],
                "business_risks": [],
                "evidence": [],
                "open_questions": [],
            },
        }
        try:
            result = self.llm.json(_SYSTEM, payload)
        except LLMError as exc:
            log_event("business_resolver.llm_error", {"error": str(exc)})
            return StageResult("BusinessResolver", self._fallback(context), [str(exc)])
        sanitized = self._sanitize(result, context)
        log_event("business_resolver.done", sanitized)
        return StageResult("BusinessResolver", sanitized)

    def _fallback(self, context: dict[str, Any]) -> dict:
        evidence = []
        for item in context.get("rag_results") or []:
            if item.get("kind") in {"business_concept", "relationship_recipe", "markdown_rule", "counting_rule"}:
                evidence.append(str(item.get("text") or "")[:1000])
        return {
            "resolved_terms": [],
            "metrics": [],
            "filters": [],
            "dimensions": [],
            "business_risks": [],
            "evidence": evidence[:6],
            "open_questions": ["BusinessResolver usou fallback; revisar evidencias RAG."],
        }

    def _sanitize(self, result: dict, context: dict[str, Any] | None = None) -> dict:
        metrics = [normalize_metric(item) for item in (result.get("metrics") or []) if isinstance(item, dict)]
        filters = [normalize_filter(item) for item in (result.get("filters") or []) if isinstance(item, dict)]
        dimensions = [normalize_dimension(item) for item in (result.get("dimensions") or []) if isinstance(item, dict)]
        metrics = _merge_metrics_from_resolved_terms(metrics, result.get("resolved_terms") or [])
        filters.extend(_filters_from_resolved_terms(result.get("resolved_terms") or []))
        return {
            "resolved_terms": result.get("resolved_terms") if isinstance(result.get("resolved_terms"), list) else [],
            "metrics": metrics,
            "filters": filters,
            "dimensions": dimensions,
            "business_risks": result.get("business_risks") if isinstance(result.get("business_risks"), list) else [],
            "evidence": result.get("evidence") if isinstance(result.get("evidence"), list) else [],
            "open_questions": result.get("open_questions") if isinstance(result.get("open_questions"), list) else [],
        }


_SYSTEM = (
    "Voce e o BusinessResolver do AgenteV2. "
    "Use apenas regras de negocio, conceitos e receitas presentes no contexto. "
    "Nao escreva SQL. Nao invente coluna. "
    "Filtros especiais devem ser representados por rule_code e rule_params, nunca por SQL bruto. "
    "Saida somente JSON."
)


def _filters_from_resolved_terms(resolved_terms: list[Any]) -> list[dict[str, Any]]:
    filters: list[dict[str, Any]] = []
    for item in resolved_terms:
        if not isinstance(item, dict):
            continue
        rule_code = str(item.get("rule_code") or "").strip()
        if not rule_code:
            entity_type = str(item.get("entity_type") or "").strip().lower()
            resolved_value = str(item.get("resolved_value") or "").strip().lower()
            human_term = str(item.get("human_term") or "").strip().lower()
            if entity_type == "rule" and any(term in f"{human_term} {resolved_value}" for term in ("ativa", "ativas", "ativo", "ativos", "atualmente")):
                rule_code = "matricula_ativa"
        if rule_code == "matricula_ativa":
            filters.append(
                {
                    "filter_name": "matricula_ativa",
                    "table": "cadastro.iptubase",
                    "column": "j01_baixa",
                    "rule_code": "matricula_ativa",
                    "description": str(item.get("description") or item.get("resolved_value") or "Matrículas sem baixa").strip(),
                }
            )
    return filters


def _merge_metrics_from_resolved_terms(metrics: list[dict[str, Any]], resolved_terms: list[Any]) -> list[dict[str, Any]]:
    output = [dict(item) for item in metrics if isinstance(item, dict)]
    for item in resolved_terms:
        if not isinstance(item, dict):
            continue
        table = str(item.get("table_name") or item.get("table") or "").strip()
        column = str(item.get("resolved_value") or item.get("column_name") or item.get("column") or "").strip()
        metric_name = str(item.get("human_term") or item.get("metric_name") or item.get("name") or "").strip()
        entity_type = str(item.get("entity_type") or "").strip().lower()
        if entity_type != "metric" or not table or not column:
            continue
        if any(existing.get("table") == table and existing.get("column") == column for existing in output):
            continue
        output.append(
            {
                "metric_name": metric_name or "quantidade",
                "table": table,
                "column": column,
                "aggregation": "COUNT_DISTINCT",
                "description": str(item.get("description") or "").strip(),
            }
        )
    return output
