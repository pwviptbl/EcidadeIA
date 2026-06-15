from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MANUAL_DIR = ROOT_DIR / "knowledge" / "manual"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "knowledge" / "rag"

IMPORTANT_TERMS = (
    "conceito",
    "conceito de negocio",
    "conceito de negócio",
    "receita de relacionamento",
    "caminho de negocio",
    "caminho de negócio",
    "papel de tabela",
    "papel da tabela",
    "regra de contagem",
    "filtro de negocio",
    "filtro de negócio",
    "resumo",
    "resumo tecnico",
    "grao",
    "grão",
    "significado da contagem",
    "relacionamento",
    "join",
    "filtro",
    "semantica",
    "semântica",
    "regra",
    "uso correto",
    "usar",
    "nao inferir",
    "não inferir",
    "nao usar",
    "não usar",
    "cuidado",
    "risco",
)

DROP_TERMS = (
    "metodo",
    "método",
    "classe",
    "auditoria",
    "campos da classe",
    "regras de inclusão",
    "regras de alteração",
    "regras de exclusão",
    "crud",
    "php",
)


def compact_text(value: str) -> str:
    return " ".join(str(value or "").split())


def title_for(path: Path, text: str) -> str:
    first_heading = re.search(r"^#{1,3}\s+(.+?)\s*$", text, flags=re.M)
    if first_heading:
        heading = first_heading.group(1).strip().strip("`")
        table = re.search(r"\b([a-z_]+)\.([a-z0-9_]+)\b", heading, flags=re.I)
        if table:
            return table.group(0).lower()
    if path.parent.name.lower() == "cadastro":
        return f"cadastro.{path.stem.lower()}"
    return path.stem.lower()


def sections(text: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    current_title = "Resumo"
    current_lines: list[str] = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match:
            if current_lines:
                result.append({"title": current_title, "content": "\n".join(current_lines).strip()})
            current_title = match.group(2).strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_lines:
        result.append({"title": current_title, "content": "\n".join(current_lines).strip()})

    return [item for item in result if compact_text(item["content"])]


def keep_section(title: str, content: str) -> bool:
    haystack = f"{title} {content}".lower()
    if any(term in haystack for term in DROP_TERMS):
        return False
    return any(term in haystack for term in IMPORTANT_TERMS)


def trim_section(content: str, max_lines: int = 14) -> str:
    kept: list[str] = []
    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if kept and kept[-1]:
                kept.append("")
            continue
        kept.append(line)
        if len([item for item in kept if item.strip()]) >= max_lines:
            break
    return "\n".join(kept).strip()


def snippet_text(table_title: str, source_label: str, text: str) -> str:
    selected: list[str] = []
    section_limit = 80 if any(
        marker in f"{table_title} {source_label}".lower()
        for marker in ("conceitos", "relacionamentos_negocio", "relacionamentos")
    ) else 8
    for section in sections(text):
        title = section["title"]
        content = section["content"]
        if not keep_section(title, content):
            continue
        title_lower = title.lower()
        max_lines = 26 if any(term in title_lower for term in ("conceito de negocio", "conceito de negócio", "receita de relacionamento")) else 14
        trimmed = trim_section(content, max_lines=max_lines)
        if trimmed:
            selected.append(f"### {title}\n\n{trimmed}")

    if not selected:
        selected.append("### Resumo operacional\n\nSem regras operacionais extraidas automaticamente. Revisar manual.")

    output = "\n\n".join(
        [
            f"## {table_title}",
            "",
            f"> Fonte manual: `{source_label}`",
            "",
            *selected[:section_limit],
            "",
        ]
    ).rstrip() + "\n"
    return output


def split_consolidated_tables(path: Path, manual_dir: Path) -> list[tuple[Path, str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+([a-z_]+\.[a-z0-9_]+)\s*$", text, flags=re.I | re.M))
    if len(matches) < 2:
        return []

    units: list[tuple[Path, str, str]] = []
    relative = path.relative_to(manual_dir)
    for index, match in enumerate(matches):
        table_name = match.group(1).lower()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        schema, table = table_name.split(".", 1)
        target_relative = Path(schema) / f"{table}.md"
        source_label = f"knowledge/manual/{relative}#{table_name}"
        units.append((target_relative, source_label, block))
    return units


def build_snippets(path: Path, manual_dir: Path) -> list[tuple[Path, str]]:
    consolidated = split_consolidated_tables(path, manual_dir)
    if consolidated:
        return [
            (relative, snippet_text(title_for(relative, text), source_label, text))
            for relative, source_label, text in consolidated
        ]

    text = path.read_text(encoding="utf-8")
    table_title = title_for(path, text)
    relative = path.relative_to(manual_dir)
    source_label = f"knowledge/manual/{relative}"
    return [(relative, snippet_text(table_title, source_label, text))]


def should_skip_manual(path: Path, manual_dir: Path) -> bool:
    relative = path.relative_to(manual_dir)
    return any(part.startswith("_") for part in relative.parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera snippets curtos para RAG a partir do manual humano.")
    parser.add_argument("--manual-dir", type=Path, default=DEFAULT_MANUAL_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    manual_dir = args.manual_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for old_file in output_dir.rglob("*.md"):
        old_file.unlink()

    count = 0
    for path in sorted(manual_dir.rglob("*.md")):
        if should_skip_manual(path, manual_dir):
            continue
        for relative, snippet in build_snippets(path, manual_dir):
            target = output_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(snippet, encoding="utf-8")
            count += 1

    print(f"snippets={count} output={output_dir}")


if __name__ == "__main__":
    main()
