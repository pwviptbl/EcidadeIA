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
from agente_v2.stages.sql_compiler import SqlCompiler  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a Fase 2 do AgenteV2 e compila SQL a partir do plano validado.")
    parser.add_argument("question", help="Pergunta do usuario")
    parser.add_argument("--json", action="store_true", help="Mostra a saida em JSON")
    args = parser.parse_args()

    phase1 = AgentV2Phase1().run(args.question)
    compiler = SqlCompiler()
    artifact = compiler.run(phase1.intent_spec, phase1.business_spec, phase1.schema_plan)
    payload = {
        "phase1": phase1.to_dict(),
        "sql_artifact": artifact.to_dict(),
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
    print("Fonte tecnica:")
    print(f"- tabelas: {', '.join(artifact.tables) if artifact.tables else 'nenhuma'}")
    print(f"- joins: {len(artifact.joins)}")
    print(f"- filtros: {len(artifact.filters)}")
    print(f"- metricas: {len(artifact.metrics)}")


if __name__ == "__main__":
    main()
