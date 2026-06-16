from __future__ import annotations

from typing import Any

from agente_v2.contracts.models import AnswerArtifact, ExecutionArtifact, SqlArtifact
from agente_v2.infrastructure.llm import LLMClient, LLMError
from agente_v2.infrastructure.logger import log_event


class AnswerSynthesizer:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    def run(
        self,
        question: str,
        phase1: dict[str, Any],
        artifact: SqlArtifact,
        execution: ExecutionArtifact,
        critic: dict[str, Any] | None = None,
        repair: dict[str, Any] | None = None,
    ) -> AnswerArtifact:
        critic = critic or {}
        repair = repair or {}
        answer = self._compose(question, phase1, artifact, execution, critic, repair)
        result = AnswerArtifact(ok=execution.ok and not critic.get("errors"), answer=answer, sql=execution.sql, notes=self._notes(artifact, execution, critic, repair))
        log_event("answer_synthesizer.done", result.to_dict())
        return result

    def _compose(
        self,
        question: str,
        phase1: dict[str, Any],
        artifact: SqlArtifact,
        execution: ExecutionArtifact,
        critic: dict[str, Any],
        repair: dict[str, Any],
    ) -> str:
        if execution.ok:
            summary = self._human_summary(question, phase1, artifact, execution)
        else:
            summary = "Nao foi possivel executar a consulta read-only."
            if execution.error:
                summary += f"\nErro: {execution.error}"

        validation_note = ""
        if critic.get("warnings"):
            validation_note = "A consulta passou com avisos."
        if critic.get("errors"):
            validation_note = "A consulta nao passou na critica."
        if validation_note:
            summary = f"{summary}\n{validation_note}"

        if repair.get("repairs"):
            summary = f"{summary}\nReparo aplicado antes da execucao."

        return f"{summary}\n\n{self._source_block(phase1, artifact, execution)}".strip()

    def _human_summary(self, question: str, phase1: dict[str, Any], artifact: SqlArtifact, execution: ExecutionArtifact) -> str:
        rows = execution.rows or []
        payload = {
            "question": question,
            "intent": phase1.get("intent_spec") or {},
            "operation": artifact.operation,
            "row_count": execution.row_count,
            "result_rows": rows[:5],
        }
        system = (
            "Voce e o sintetizador final do AgenteV2. "
            "Escreva uma resposta curta em pt-BR, objetiva e humana. "
            "Explique o resultado com base apenas nos dados recebidos. "
            "Se houver numeros, destaque a variacao principal e os fatores explicativos. "
            "Nao mencione SQL nem detalhes internos."
        )
        try:
            text = self.llm.text(system, payload)
        except LLMError:
            return self._fallback_summary(execution)
        cleaned = str(text or "").strip()
        return cleaned or self._fallback_summary(execution)

    def _fallback_summary(self, execution: ExecutionArtifact) -> str:
        if execution.row_count == 1:
            return "Resultado retornado com 1 linha."
        return f"Resultado retornado com {execution.row_count} linhas."

    def _source_block(self, phase1: dict[str, Any], artifact: SqlArtifact, execution: ExecutionArtifact) -> str:
        tables = ", ".join(artifact.tables) if artifact.tables else "nenhuma"
        filters = artifact.filters or []
        filter_names = ", ".join(str(item.get("filter_name") or item.get("column") or "") for item in filters if isinstance(item, dict) and (item.get("filter_name") or item.get("column")))
        source_lines = [
            "Fonte dos dados",
            f"- operacao: {artifact.operation}",
            f"- tabelas: {tables}",
            f"- filtros: {filter_names or 'nenhum'}",
            f"- linhas: {execution.row_count}",
        ]
        return "<details><summary>Fonte tecnica e SQL usada</summary>\n\n" + "\n".join(source_lines) + "\n\n```sql\n" + execution.sql + "\n```\n\n</details>"

    def _notes(self, artifact: SqlArtifact, execution: ExecutionArtifact, critic: dict[str, Any], repair: dict[str, Any]) -> list[str]:
        notes = list(artifact.notes or [])
        if critic.get("warnings"):
            notes.append("Consulta executada com avisos da critica.")
        if repair.get("repairs"):
            notes.append("Consulta passou por reparo deterministico.")
        if not execution.ok and execution.error:
            notes.append("Execucao falhou.")
        return notes
