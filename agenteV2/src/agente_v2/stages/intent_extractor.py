from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
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
        text = _normalize_text(question)
        tokens = re.findall(r"[a-z0-9]+", text)
        years = [int(item) for item in re.findall(r"\b(20\d{2})\b", text)]
        ranking_direction = ""
        ranking_limit = 0
        if len(years) >= 2 and _contains_keyword(text, tokens, ("compare", "compar", "aumento", "variacao", "variação")):
            intent = "compare_periods"
        elif _contains_keyword(text, tokens, ("maior", "menor", "top", "ranking", "melhor", "pior", "mais alto", "mais baixo", "meior")):
            intent = "ranking"
            ranking_direction, ranking_limit = _infer_ranking_hint(text)
        elif _contains_keyword(text, tokens, ("quantos", "quantas", "quantidade", "total", "contagem", "quantas matrículas", "quantidade de")):
            intent = "count_by_dimension"
        elif _contains_keyword(text, tokens, ("soma", "valor", "total")):
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
    text = _normalize_text(text)
    tokens = re.findall(r"[a-z0-9]+", text)
    direction = "DESC"
    if _contains_keyword(text, tokens, ("menor", "menos", "pior", "mais baixo")):
        direction = "ASC"
    limit = 10
    match = re.search(r"\btop\s*(\d+)\b", text)
    if not match:
        match = re.search(r"\bprimeir[oa]s?\s*(\d+)\b", text)
    if match:
        limit = max(1, int(match.group(1)))
    elif _contains_keyword(text, tokens, ("maior", "menor", "melhor", "pior", "meior")):
        limit = 1
    return direction, limit


def _contains_keyword(text: str, tokens: list[str], keywords: tuple[str, ...]) -> bool:
    for keyword in keywords:
        normalized = _normalize_text(keyword).strip()
        if not normalized:
            continue
        if " " in normalized:
            if normalized in text:
                return True
            continue
        if normalized in tokens:
            return True
        for token in tokens:
            if SequenceMatcher(None, normalized, token).ratio() >= 0.84:
                return True
    return False


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))
