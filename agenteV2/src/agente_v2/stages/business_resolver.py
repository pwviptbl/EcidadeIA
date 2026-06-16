from __future__ import annotations

from typing import Any

from agente_v2.context import compact_context
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
                "Nao gere SQL. Retorne regras, metricas, filtros e riscos em JSON."
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
        sanitized = self._sanitize(result)
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

    def _sanitize(self, result: dict) -> dict:
        return {
            "resolved_terms": result.get("resolved_terms") if isinstance(result.get("resolved_terms"), list) else [],
            "metrics": result.get("metrics") if isinstance(result.get("metrics"), list) else [],
            "filters": result.get("filters") if isinstance(result.get("filters"), list) else [],
            "dimensions": result.get("dimensions") if isinstance(result.get("dimensions"), list) else [],
            "business_risks": result.get("business_risks") if isinstance(result.get("business_risks"), list) else [],
            "evidence": result.get("evidence") if isinstance(result.get("evidence"), list) else [],
            "open_questions": result.get("open_questions") if isinstance(result.get("open_questions"), list) else [],
        }


_SYSTEM = (
    "Voce e o BusinessResolver do AgenteV2. "
    "Use apenas regras de negocio, conceitos e receitas presentes no contexto. "
    "Nao escreva SQL. Nao invente coluna. Saida somente JSON."
)
