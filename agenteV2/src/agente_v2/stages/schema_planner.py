from __future__ import annotations

from typing import Any

from agente_v2.context import compact_context
from agente_v2.contracts.models import IntentSpec, StageResult
from agente_v2.infrastructure.llm import LLMClient, LLMError
from agente_v2.infrastructure.logger import log_event


class SchemaPlanner:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, question: str, intent: IntentSpec, business: dict, context: dict[str, Any]) -> StageResult:
        payload = {
            "task": (
                "Monte um plano de esquema para responder a pergunta. "
                "Escolha tabelas, grao, eixo temporal, joins e agrupamentos. "
                "Nao escreva SQL."
            ),
            "question": question,
            "intent_spec": intent.to_dict(),
            "business_spec": business,
            "context": compact_context(context),
            "response_schema": {
                "entity": "entidade principal",
                "grain": [],
                "time_axis": {"table": "schema.tabela", "column": "coluna"},
                "tables": [],
                "joins": [],
                "group_by": [],
                "metrics": [],
                "filters": [],
                "risks": [],
                "open_questions": [],
            },
        }
        try:
            result = self.llm.json(_SYSTEM, payload)
        except LLMError as exc:
            log_event("schema_planner.llm_error", {"error": str(exc)})
            return StageResult("SchemaPlanner", self._fallback(context), [str(exc)])
        sanitized = self._sanitize(result)
        log_event("schema_planner.done", sanitized)
        return StageResult("SchemaPlanner", sanitized)

    def _fallback(self, context: dict[str, Any]) -> dict:
        tables = context.get("tables") or []
        return {
            "entity": "",
            "grain": [],
            "time_axis": {},
            "tables": tables[:6],
            "joins": [],
            "group_by": [],
            "metrics": [],
            "filters": [],
            "risks": ["SchemaPlanner usou fallback; plano incompleto."],
            "open_questions": ["Validar grao, metricas, filtros e joins."],
        }

    def _sanitize(self, result: dict) -> dict:
        return {
            "entity": str(result.get("entity") or ""),
            "grain": result.get("grain") if isinstance(result.get("grain"), list) else [],
            "time_axis": result.get("time_axis") if isinstance(result.get("time_axis"), dict) else {},
            "tables": result.get("tables") if isinstance(result.get("tables"), list) else [],
            "joins": result.get("joins") if isinstance(result.get("joins"), list) else [],
            "group_by": result.get("group_by") if isinstance(result.get("group_by"), list) else [],
            "metrics": result.get("metrics") if isinstance(result.get("metrics"), list) else [],
            "filters": result.get("filters") if isinstance(result.get("filters"), list) else [],
            "risks": result.get("risks") if isinstance(result.get("risks"), list) else [],
            "open_questions": result.get("open_questions") if isinstance(result.get("open_questions"), list) else [],
        }


_SYSTEM = (
    "Voce e o SchemaPlanner do AgenteV2. "
    "Planeje tabelas e relacionamentos sem escrever SQL. "
    "Use somente tabelas e colunas do contexto. Se faltar evidencia, marque open_questions. "
    "Saida somente JSON."
)
