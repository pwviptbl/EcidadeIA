from __future__ import annotations

import re
from typing import Any

from agente_v2.contracts.models import IntentSpec
from agente_v2.infrastructure.llm import LLMClient, LLMError
from agente_v2.infrastructure.logger import log_event


class IntentExtractor:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, question: str) -> IntentSpec:
        payload = {
            "task": "Extraia a intencao da pergunta. Nao escolha tabelas e nao escreva SQL.",
            "question": question,
            "allowed_intents": [
                "compare_periods",
                "count_by_dimension",
                "sum_by_dimension",
                "detail_listing",
                "ranking",
                "knowledge_review",
            ],
            "response_schema": {
                "intent": "string",
                "confidence": "0..1",
                "years": [2025, 2026],
                "ranking_direction": "ASC|DESC",
                "ranking_limit": 10,
                "literal_filters": ["filtros citados literalmente"],
                "requested_entities": ["entidades de negocio"],
                "requested_metrics": ["metricas pedidas"],
                "requested_dimensions": ["dimensoes pedidas"],
                "ambiguities": ["ambiguidades"],
            },
        }
        try:
            result = self.llm.json(_SYSTEM, payload)
            spec = IntentSpec.from_dict(result)
        except LLMError as exc:
            log_event("intent.llm_error", {"error": str(exc)})
            spec = self._fallback(question)
        log_event("intent.done", spec.to_dict())
        return spec

    def _fallback(self, question: str) -> IntentSpec:
        text = question.lower()
        years = [int(item) for item in re.findall(r"\b(20\d{2})\b", text)]
        ranking_direction = ""
        ranking_limit = 0
        if len(years) >= 2 and any(term in text for term in ("compare", "compar", "aumento", "variacao", "variação")):
            intent = "compare_periods"
        elif any(term in text for term in ("maior", "menor", "top", "ranking", "melhor", "pior", "mais alto", "mais baixo")):
            intent = "ranking"
            ranking_direction, ranking_limit = _infer_ranking_hint(text)
        elif any(term in text for term in ("quantos", "quantas", "quantidade", "total de")):
            intent = "count_by_dimension" if "por " in text else "detail_listing"
        elif any(term in text for term in ("soma", "valor", "total")):
            intent = "sum_by_dimension"
        else:
            intent = "knowledge_review"
        return IntentSpec(
            intent=intent,
            confidence=0.35,
            years=years[:4],
            ranking_direction=ranking_direction,
            ranking_limit=ranking_limit,
            ambiguities=["fallback lexical usado"],
        )


_SYSTEM = (
    "Voce e o IntentExtractor do AgenteV2. "
    "Sua saida deve ser JSON valido. "
    "Nao escreva SQL. Nao resolva tabelas. Nao explique."
)


def _infer_ranking_hint(text: str) -> tuple[str, int]:
    direction = "DESC"
    if any(term in text for term in ("menor", "menos", "pior", "mais baixo")):
        direction = "ASC"
    limit = 10
    match = re.search(r"\btop\s*(\d+)\b", text)
    if not match:
        match = re.search(r"\bprimeir[oa]s?\s*(\d+)\b", text)
    if match:
        limit = max(1, int(match.group(1)))
    elif any(term in text for term in ("maior", "menor", "melhor", "pior")):
        limit = 1
    return direction, limit
