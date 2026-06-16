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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Executa a Fase 1 do AgenteV2 sem gerar SQL.")
    parser.add_argument("question", nargs="*", help="Pergunta do usuario.")
    parser.add_argument("--json", action="store_true", help="Imprime payload JSON completo.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    question = " ".join(args.question).strip()
    if not question:
        raise SystemExit("Informe a pergunta.")

    result = AgentV2Phase1().run(question)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(summarize_phase1(result))


if __name__ == "__main__":
    main()
