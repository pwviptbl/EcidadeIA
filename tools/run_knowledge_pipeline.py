from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT_DIR / "tools"


def run(command: list[str]) -> None:
    printable = " ".join(command)
    print(f"[pipeline] {printable}", flush=True)
    subprocess.run(command, cwd=ROOT_DIR, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa a sequencia de geracao do conhecimento operacional e do RAG."
    )
    parser.add_argument("--schema", default="cadastro", help="Schema alvo para extracao/export. Use 'all' para todos.")
    parser.add_argument(
        "--from-db",
        action="store_true",
        help="Executa tambem a extracao do catalogo a partir do banco. Exige tools/.env configurado.",
    )
    parser.add_argument(
        "--skip-knowledge-rag",
        action="store_true",
        help="Nao regenera knowledge/rag a partir de knowledge/manual.",
    )
    parser.add_argument(
        "--skip-rag-documents",
        action="store_true",
        help="Nao regenera rag/catalog_documents.jsonl.",
    )
    parser.add_argument(
        "--export-obsidian",
        action="store_true",
        help="Exporta catalogo JSON para Markdown em docs/exemplos/obsidian.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    python = sys.executable

    if args.from_db:
        extract_cmd = [python, str(TOOLS_DIR / "extract_catalog.py"), "--schema", args.schema]
        if args.schema.lower() != "all":
            extract_cmd.extend(["--output", str(ROOT_DIR / "catalog" / f"{args.schema}_extraido.json")])
        else:
            extract_cmd.extend(["--output-dir", str(ROOT_DIR / "catalog")])
        run(extract_cmd)

    if args.export_obsidian:
        run(
            [
                python,
                str(TOOLS_DIR / "export_catalog_markdown.py"),
                "--domain",
                args.schema,
                "--catalog-dir",
                str(ROOT_DIR / "catalog"),
                "--output-dir",
                str(ROOT_DIR / "docs" / "exemplos" / "obsidian"),
            ]
        )

    if not args.skip_knowledge_rag:
        run(
            [
                python,
                str(TOOLS_DIR / "build_knowledge_rag.py"),
                "--manual-dir",
                str(ROOT_DIR / "knowledge" / "manual"),
                "--output-dir",
                str(ROOT_DIR / "knowledge" / "rag"),
            ]
        )

    if not args.skip_rag_documents:
        run([python, str(TOOLS_DIR / "build_rag_documents.py")])


if __name__ == "__main__":
    main()
