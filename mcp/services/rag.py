from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from config import RAG_DOCUMENTS_PATH
from services.logger import log_event


STOPWORDS = {
    "a",
    "as",
    "o",
    "os",
    "um",
    "uma",
    "de",
    "do",
    "da",
    "dos",
    "das",
    "e",
    "em",
    "no",
    "na",
    "nos",
    "nas",
    "para",
    "por",
    "com",
    "que",
    "qual",
    "quais",
    "quanto",
    "quantos",
    "quantas",
    "tem",
    "temos",
    "existe",
    "existem",
    "compare",
    "comparar",
    "explique",
    "explicar",
    "principais",
    "principai",
    "principal",
    "fatores",
    "fator",
    "aumento",
    "aumentos",
    "reducao",
    "redução",
    "variacao",
    "variação",
    "evolucao",
    "evolução",
}

KIND_WEIGHTS = {
    "table": 1.35,
    "column": 1.0,
    "metric": 1.45,
    "relationship": 0.75,
    "intent": 0.65,
    "example": 1.2,
    "business_rule": 1.75,
    "classification": 1.85,
    "filter_semantics": 1.9,
    "validated_query": 2.0,
    "grouping_rule": 1.55,
    "markdown_rule": 2.15,
    "markdown_sql": 1.95,
    "markdown_reference": 1.35,
}


class RagIndex:
    def __init__(self, path: Path = RAG_DOCUMENTS_PATH):
        self.path = path
        self.documents: list[dict[str, Any]] = []
        self.doc_terms: list[Counter[str]] = []
        self.doc_lengths: list[int] = []
        self.idf: dict[str, float] = {}
        self.avgdl = 0.0
        self.loaded = False
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            log_event("rag.missing", {"path": str(self.path)})
            return

        dfs: Counter[str] = Counter()
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                document = json.loads(line)
                terms = Counter(tokenize(document.get("text", "")))
                if not terms:
                    continue
                self.documents.append(document)
                self.doc_terms.append(terms)
                length = sum(terms.values())
                self.doc_lengths.append(length)
                dfs.update(terms.keys())

        total = len(self.documents)
        if not total:
            return

        self.avgdl = sum(self.doc_lengths) / total
        self.idf = {
            term: math.log(1 + (total - df + 0.5) / (df + 0.5))
            for term, df in dfs.items()
        }
        self.loaded = True
        counts: Counter[str] = Counter(str(doc.get("kind") or "") for doc in self.documents)
        log_event(
            "rag.loaded",
            {
                "path": str(self.path),
                "documents": total,
                "kinds": dict(counts),
            },
        )

    def search(self, query: str, limit: int = 20, kinds: list[str] | None = None) -> list[dict[str, Any]]:
        if not self.loaded:
            return []

        query_terms = tokenize(query)
        if not query_terms:
            return []

        allowed_kinds = {str(kind) for kind in kinds} if kinds else None
        scored = []
        for index, document in enumerate(self.documents):
            kind = str(document.get("kind") or "")
            if allowed_kinds and kind not in allowed_kinds:
                continue
            score = self._bm25_score(query_terms, index)
            if not score:
                continue
            score *= KIND_WEIGHTS.get(kind, 1.0)
            score += self._metadata_boost(query_terms, document)
            if score:
                scored.append((score, document))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "id": document.get("id"),
                "kind": document.get("kind"),
                "score": round(score, 4),
                "text": document.get("text"),
                "metadata": document.get("metadata") or {},
            }
            for score, document in scored[: max(1, min(int(limit or 20), 100))]
        ]

    def search_tables(self, query: str, catalog, limit: int = 20) -> list[dict[str, Any]]:
        documents = self.search(query, limit=max(limit * 8, 40))
        grouped: dict[str, dict[str, Any]] = {}
        for document in documents:
            metadata = document.get("metadata") or {}
            table_name = metadata.get("table")
            if not table_name or table_name not in catalog.data.get("tables", {}):
                continue

            group = grouped.setdefault(
                table_name,
                {
                    "table": table_name,
                    "score": 0.0,
                    "scores": [],
                    "evidence": [],
                },
            )
            doc_score = float(document.get("score") or 0)
            group["scores"].append(doc_score)
            if len(group["evidence"]) < 5:
                evidence_text = first_line(document.get("text"))
                if document.get("kind") in {
                    "business_rule",
                    "classification",
                    "filter_semantics",
                    "validated_query",
                    "grouping_rule",
                    "markdown_rule",
                    "markdown_sql",
                    "markdown_reference",
                }:
                    evidence_text = compact_document_text(document.get("text"), limit=700)
                group["evidence"].append(
                    {
                        "kind": document.get("kind"),
                        "score": doc_score,
                        "column": metadata.get("column"),
                        "metric": metadata.get("metric"),
                        "text": evidence_text,
                    }
                )

        results = []
        for table_name, group in grouped.items():
            info = catalog.data["tables"][table_name]
            scores = sorted(group["scores"], reverse=True)
            score = (scores[0] if scores else 0.0) + sum(scores[1:4]) * 0.15
            score += self._table_name_boost(query, table_name)
            score += self._catalog_structure_boost(query, info)
            if info.get("recommended"):
                score *= 1.15
            results.append(
                {
                    "table": table_name,
                    "description": info.get("description"),
                    "columns": info.get("columns", {}),
                    "grain": info.get("grain", []),
                    "entity_key": info.get("entity_key", []),
                    "time_key": info.get("time_key"),
                    "default_filters": info.get("default_filters", []),
                    "recommended": bool(info.get("recommended")),
                    "score": int(round(score * 10)),
                    "rag_evidence": group["evidence"],
                }
            )

        results.sort(key=lambda item: (item["score"], item["recommended"]), reverse=True)
        return results[: max(1, min(int(limit or 20), 100))]

    def _table_name_boost(self, query: str, table_name: str) -> float:
        terms = tokenize(query)
        leaf = table_name.split(".", 1)[-1].lower()
        boost = 0.0
        for term in terms:
            if leaf.startswith(term):
                boost += 8.0
            elif term in leaf:
                boost += 2.0
        return boost

    def _catalog_structure_boost(self, query: str, table_info: dict[str, Any]) -> float:
        query_text = str(query or "").lower()
        temporal_question = bool(re.search(r"\b(19|20)\d{2}\b", query_text)) or any(
            term in query_text
            for term in ("compar", "period", "exercicio", "exercício", "ano", "evolu", "variac", "variaç")
        )
        variation_question = any(
            term in query_text
            for term in ("aumento", "redu", "variac", "variaç", "fator", "evolu", "compar")
        )

        columns = table_info.get("columns") or {}
        if not isinstance(columns, dict):
            return 0.0

        temporal_columns = 0
        entity_columns = 0
        numeric_columns = 0
        for column_name, column in columns.items():
            column = column if isinstance(column, dict) else {"description": column}
            name = str(column_name or "").lower()
            description = str(column.get("description") or "").lower()
            data_type = str(column.get("type") or "").lower()
            haystack = f"{name} {description}"
            if any(token in haystack for token in ("ano", "anousu", "exercicio", "exercício", "data", "dt")):
                temporal_columns += 1
            if any(token in haystack for token in ("matric", "codigo", "código", "sequencial", "id")):
                entity_columns += 1
            if any(token in data_type for token in ("int", "numeric", "double", "real", "decimal")):
                numeric_columns += 1

        boost = 0.0
        if temporal_question and temporal_columns:
            boost += min(temporal_columns, 3) * 3.0
        if variation_question and numeric_columns >= 3:
            boost += min(numeric_columns, 8) * 1.2
        if temporal_question and entity_columns and temporal_columns:
            boost += 3.0
        primary_key = [str(item).lower() for item in (table_info.get("primary_key") or [])]
        pk_has_temporal = any(any(token in item for token in ("ano", "anousu", "exercicio", "data", "dt")) for item in primary_key)
        pk_has_entity = any(
            any(token in item for token in ("matric", "cgm", "inscr", "id", "codigo", "código"))
            for item in primary_key
        )
        if primary_key and len(primary_key) >= 2:
            boost += 1.5
        if temporal_question and pk_has_temporal:
            boost += 4.0
        if temporal_question and pk_has_temporal and pk_has_entity:
            boost += 8.0
        return boost

    def _bm25_score(self, query_terms: list[str], index: int) -> float:
        terms = self.doc_terms[index]
        length = self.doc_lengths[index]
        if not length:
            return 0.0

        k1 = 1.5
        b = 0.75
        score = 0.0
        for term in query_terms:
            freq = terms.get(term, 0)
            if not freq:
                continue
            denominator = freq + k1 * (1 - b + b * length / (self.avgdl or 1))
            score += self.idf.get(term, 0.0) * (freq * (k1 + 1)) / denominator
        return score

    def _metadata_boost(self, query_terms: list[str], document: dict[str, Any]) -> float:
        metadata = document.get("metadata") or {}
        values = [
            metadata.get("table"),
            metadata.get("column"),
            metadata.get("metric"),
            metadata.get("intent"),
            metadata.get("domain"),
        ]
        tokens = set()
        for value in values:
            tokens.update(tokenize(value))
        boost = sum(0.4 for term in query_terms if term in tokens)

        table = str(metadata.get("table") or "").lower()
        table_leaf = table.split(".", 1)[-1]
        column = str(metadata.get("column") or "").lower()
        for term in query_terms:
            if table_leaf.startswith(term):
                boost += 2.5
            elif term in table_leaf:
                boost += 0.8
            if column.startswith(term):
                boost += 1.0
            elif term in column:
                boost += 0.3
        return boost


def tokenize(value: Any) -> list[str]:
    tokens = []
    for raw in re.findall(r"[a-zA-ZÀ-ÿ0-9_]+", str(value or "").lower()):
        normalized = strip_plural(raw)
        if raw in STOPWORDS or len(normalized) < 2 or normalized.isdigit() or normalized in STOPWORDS:
            continue
        tokens.append(normalized)
    return tokens


def strip_plural(value: str) -> str:
    if len(value) > 3 and value.endswith("s"):
        return value[:-1]
    return value


def first_line(value: Any) -> str:
    return str(value or "").strip().splitlines()[0][:240]


def compact_document_text(value: Any, limit: int = 700) -> str:
    return " ".join(str(value or "").split())[:limit]
