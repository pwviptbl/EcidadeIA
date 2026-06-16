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
        "--skip-validate",
        action="store_true",
        help="Nao valida o padrao dos manuais/RAG apos a geracao.",
    )
    parser.add_argument(
        "--export-obsidian",
        action="store_true",
        help="Exporta catalogo JSON para Markdown em docs/exemplos/obsidian.",
    )
    parser.add_argument(
        "--export-business-scaffold",
        action="store_true",
        help="Gera esqueletos de conceitos e relacionamentos de negocio em docs/exemplos/obsidian.",
    )
    parser.add_argument(
        "--skip-business-scaffold",
        action="store_true",
        help="Nao gera os esqueletos de curadoria de negocio ao exportar para Obsidian.",
    )
    parser.add_argument(
        "--overwrite-business-scaffold",
        action="store_true",
        help="Sobrescreve esqueletos de negocio ja existentes.",
    )
    parser.add_argument("--max-concept-tables", type=int, default=20)
    parser.add_argument("--max-relationship-recipes", type=int, default=80)
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

    if (args.export_obsidian or args.export_business_scaffold) and not args.skip_business_scaffold:
        scaffold_cmd = [
            python,
            str(TOOLS_DIR / "scaffold_business_knowledge.py"),
            "--domain",
            args.schema,
            "--catalog-dir",
            str(ROOT_DIR / "catalog"),
            "--output-dir",
            str(ROOT_DIR / "docs" / "exemplos" / "obsidian"),
            "--max-concept-tables",
            str(args.max_concept_tables),
            "--max-relationship-recipes",
            str(args.max_relationship_recipes),
        ]
        if args.overwrite_business_scaffold:
            scaffold_cmd.append("--overwrite")
        run(scaffold_cmd)

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

    if not args.skip_validate:
        run(
            [
                python,
                str(TOOLS_DIR / "validate_knowledge_manual.py"),
                "--schema",
                args.schema if args.schema.lower() != "all" else "cadastro",
            ]
        )


if __name__ == "__main__":
    main()
