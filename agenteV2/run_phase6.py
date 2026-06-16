#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agente_v2.orchestrator import AgentV2Phase1, summarize_phase1  # noqa: E402
from agente_v2.stages.answer_synthesizer import AnswerSynthesizer  # noqa: E402
from agente_v2.stages.executor import Executor  # noqa: E402
from agente_v2.stages.repair_loop import RepairLoop  # noqa: E402
from agente_v2.stages.sql_compiler import SqlCompiler  # noqa: E402
from agente_v2.stages.sql_critic import SqlCritic  # noqa: E402
from agente_v2.infrastructure.llm import LLMClient  # noqa: E402


class LoadedPhase1:
    def __init__(self, data: dict):
        self.question = str(data.get("question") or "")
        self.intent_spec = data.get("intent_spec") or {}
        self.business_spec = data.get("business_spec") or {}
        self.schema_plan = data.get("schema_plan") or {}
        self.validation = data.get("validation") or {}
        self.context = data.get("context") or {}
        self._data = data

    def to_dict(self) -> dict:
        return self._data


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a Fase 6 do AgenteV2: resposta humana com SQL recolhivel.")
    parser.add_argument("question", nargs="*", help="Pergunta do usuario")
    parser.add_argument("--phase1-json", help="Caminho para um JSON salvo da Fase 1")
    parser.add_argument("--json", action="store_true", help="Mostra a saida em JSON")
    args = parser.parse_args()

    if args.phase1_json:
        phase1_data = json.loads(Path(args.phase1_json).read_text(encoding="utf-8"))
        phase1 = LoadedPhase1(phase1_data)
    else:
        question = " ".join(args.question).strip()
        phase1 = AgentV2Phase1().run(question)

    artifact = SqlCompiler().run(phase1.intent_spec, phase1.business_spec, phase1.schema_plan, question=phase1.question)
    critic = SqlCritic().run(artifact, phase1.business_spec, phase1.schema_plan)
    repair = RepairLoop().run(phase1.intent_spec, phase1.business_spec, phase1.schema_plan, artifact, critic)
    execution = Executor().run(artifact, sql=repair.repaired_sql)
    answer = AnswerSynthesizer(LLMClient()).run(phase1.question, phase1.to_dict(), artifact, execution, critic.to_dict(), repair.to_dict())

    payload = {
        "phase1": phase1.to_dict(),
        "sql_artifact": artifact.to_dict(),
        "critic": critic.to_dict(),
        "repair": repair.to_dict(),
        "execution": execution.to_dict(),
        "answer": answer.to_dict(),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return

    print(summarize_phase1(phase1))
    print("")
    print("Resposta")
    print(answer.answer)


if __name__ == "__main__":
    main()
