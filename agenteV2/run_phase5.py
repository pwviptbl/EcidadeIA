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
from agente_v2.stages.executor import Executor  # noqa: E402
from agente_v2.stages.repair_loop import RepairLoop  # noqa: E402
from agente_v2.stages.sql_compiler import SqlCompiler  # noqa: E402
from agente_v2.stages.sql_critic import SqlCritic  # noqa: E402


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
    parser = argparse.ArgumentParser(description="Executa a Fase 5 do AgenteV2: compilacao, critica, reparo e execucao read-only.")
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

    artifact = SqlCompiler().run(phase1.intent_spec, phase1.business_spec, phase1.schema_plan)
    critic = SqlCritic().run(artifact, phase1.business_spec, phase1.schema_plan)
    repair = RepairLoop().run(phase1.intent_spec, phase1.business_spec, phase1.schema_plan, artifact, critic)
    execution = Executor().run(artifact, sql=repair.repaired_sql)

    payload = {
        "phase1": phase1.to_dict(),
        "sql_artifact": artifact.to_dict(),
        "critic": critic.to_dict(),
        "repair": repair.to_dict(),
        "execution": execution.to_dict(),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return

    print(summarize_phase1(phase1))
    print("")
    print("AgenteV2 Fase 2: SQL compilado.")
    print(f"Operacao: {artifact.operation}")
    print(f"Linhas maximas: {artifact.limit}")
    print("")
    print(artifact.sql)
    print("")
    print("AgenteV2 Fase 3: critica da SQL.")
    print(f"- ok: {critic.ok}")
    for error in critic.errors:
        print(f"- erro: {error}")
    for warning in critic.warnings:
        print(f"- aviso: {warning}")
    for note in critic.notes:
        print(f"- nota: {note}")
    print("")
    print("AgenteV2 Fase 4: reparo.")
    print(f"- ok: {repair.ok}")
    print(f"- tentativas: {repair.attempts}")
    for item in repair.repairs:
        print(f"- reparo: {item}")
    print("")
    print(repair.repaired_sql)
    print("")
    print("AgenteV2 Fase 5: execucao read-only.")
    print(f"- ok: {execution.ok}")
    print(f"- rows: {execution.row_count}")
    print(f"- duration_ms: {execution.duration_ms}")
    if execution.error:
        print(f"- erro: {execution.error}")


if __name__ == "__main__":
    main()
