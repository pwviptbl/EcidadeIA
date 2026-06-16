from __future__ import annotations

from typing import Any

from agente_v2.context import build_context, compact_context
from agente_v2.contracts.models import Phase1Result
from agente_v2.infrastructure.llm import LLMClient
from agente_v2.infrastructure.logger import log_event
from agente_v2.infrastructure.mcp import McpClient
from agente_v2.stages.business_resolver import BusinessResolver
from agente_v2.stages.intent_extractor import IntentExtractor
from agente_v2.stages.plan_validator import PlanValidator
from agente_v2.stages.schema_planner import SchemaPlanner


class AgentV2Phase1:
    """
    Fase 1: entender a pergunta e montar plano validavel.

    Esta classe nao compila SQL e nao executa consulta. O ponto de parada
    intencional e o resultado do PlanValidator.
    """

    def __init__(self, mcp: McpClient | None = None, planner_llm: LLMClient | None = None):
        self.mcp = mcp or McpClient()
        self.llm = planner_llm or LLMClient()
        self.intent_extractor = IntentExtractor(self.llm)
        self.business_resolver = BusinessResolver(self.llm)
        self.schema_planner = SchemaPlanner(self.llm)
        self.plan_validator = PlanValidator()

    def run(self, question: str) -> Phase1Result:
        question = question.strip()
        if not question:
            raise ValueError("Pergunta vazia.")

        log_event("phase1.start", {"question": question})
        context = build_context(question, self.mcp)
        intent = self.intent_extractor.run(question)
        business = self.business_resolver.run(question, intent, context)
        schema = self.schema_planner.run(question, intent, business.payload, context)
        validation = self.plan_validator.run(schema.payload, business.payload, context)
        result = Phase1Result(
            question=question,
            intent_spec=intent.to_dict(),
            business_spec=business.payload,
            schema_plan=schema.payload,
            validation=validation.payload,
            context=compact_context(context),
        )
        log_event("phase1.done", {"validation_ok": validation.payload.get("ok"), "errors": validation.payload.get("errors")})
        return result


def summarize_phase1(result: Phase1Result) -> str:
    data = result.to_dict()
    lines = [
        "AgenteV2 Fase 1: plano gerado sem SQL.",
        "",
        f"Intent: {data['intent_spec'].get('intent')} | confianca={data['intent_spec'].get('confidence')}",
        f"Anos: {data['intent_spec'].get('years')}",
        f"Tabelas candidatas: {', '.join(data['context'].get('tables') or []) or 'nenhuma'}",
        "",
        "BusinessSpec:",
        f"- termos resolvidos: {len(data['business_spec'].get('resolved_terms') or [])}",
        f"- metricas: {len(data['business_spec'].get('metrics') or [])}",
        f"- filtros: {len(data['business_spec'].get('filters') or [])}",
        f"- riscos: {len(data['business_spec'].get('business_risks') or [])}",
        f"- evidencias: {len(data['business_spec'].get('evidence') or [])}",
        "",
        "SchemaPlan:",
        f"- entidade: {data['schema_plan'].get('entity') or 'nao informada'}",
        f"- grao: {', '.join(data['schema_plan'].get('grain') or []) or 'nao informado'}",
        f"- tabelas: {', '.join(data['schema_plan'].get('tables') or []) or 'nenhuma'}",
        f"- joins: {len(data['schema_plan'].get('joins') or [])}",
        f"- metricas: {len(data['schema_plan'].get('metrics') or [])}",
        "",
        "Validacao:",
        f"- ok: {data['validation'].get('ok')}",
    ]
    for error in data["validation"].get("errors") or []:
        lines.append(f"- erro: {error}")
    for warning in data["validation"].get("warnings") or []:
        lines.append(f"- aviso: {warning}")
    return "\n".join(lines)
