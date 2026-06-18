from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MANUAL_DIR = ROOT_DIR / "knowledge" / "manual"
DEFAULT_RAG_DIR = ROOT_DIR / "knowledge" / "rag"
TABLE_SKIP_NAMES = {"conceitos.md", "relacionamentos_negocio.md"}

FORBIDDEN_PATTERNS = (
    re.compile(r"```sql", re.I),
    re.compile(r"^\s*(select|with|insert|update|delete)\s+", re.I | re.M),
    re.compile(r"consultas?\s+sql\s+prontas?", re.I),
    re.compile(r"queries\s+sql\s+prontas?", re.I),
    re.compile(r"sqls?\s+(extra[ií]dos|normalizados|de referencia|de referência)", re.I),
    re.compile(r"sql_exemplo", re.I),
    re.compile(r"sql\s+validada", re.I),
)


def validate_no_sql_ready(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []
    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"{path}: padrao proibido encontrado: {match.group(0)!r}")
    return errors


def validate_table_heading(path: Path, schema: str) -> list[str]:
    if path.name in TABLE_SKIP_NAMES or path.name.startswith("_"):
        return []
    text = path.read_text(encoding="utf-8")
    first_line = text.splitlines()[0].strip() if text.splitlines() else ""
    if re.match(r"^#\s+Conceito de neg[oó]cio:\s+\S+", first_line, flags=re.I):
        return []
    expected = f"# Tabela de negocio: `{schema}.{path.stem}`"
    if first_line != expected:
        return [f"{path}: cabecalho esperado {expected!r}, encontrado {first_line!r}"]
    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida padrao humano de conhecimento para o agente.")
    parser.add_argument("--manual-dir", type=Path, default=DEFAULT_MANUAL_DIR)
    parser.add_argument("--rag-dir", type=Path, default=DEFAULT_RAG_DIR)
    parser.add_argument("--schema", default="cadastro")
    parser.add_argument("--skip-rag", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manual_dir = args.manual_dir.resolve()
    rag_dir = args.rag_dir.resolve()
    schema = args.schema.strip()
    errors: list[str] = []

    for path in sorted(manual_dir.rglob("*.md")):
        if any(part.startswith("_") for part in path.relative_to(manual_dir).parts):
            continue
        errors.extend(validate_no_sql_ready(path))

    schema_dir = manual_dir / schema
    if schema_dir.exists():
        for path in sorted(schema_dir.glob("*.md")):
            errors.extend(validate_table_heading(path, schema))

    if not args.skip_rag and rag_dir.exists():
        for path in sorted(rag_dir.rglob("*.md")):
            errors.extend(validate_no_sql_ready(path))

    if errors:
        for error in errors:
            print(f"[knowledge-validate] {error}")
        raise SystemExit(1)

    print("[knowledge-validate] ok")


if __name__ == "__main__":
    main()
