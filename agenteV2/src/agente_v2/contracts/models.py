from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def clean_list(value: Any) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


@dataclass
class IntentSpec:
    intent: str = "knowledge_review"
    confidence: float = 0.0
    years: list[int] = field(default_factory=list)
    literal_filters: list[str] = field(default_factory=list)
    requested_entities: list[str] = field(default_factory=list)
    requested_metrics: list[str] = field(default_factory=list)
    requested_dimensions: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict | None) -> "IntentSpec":
        data = data or {}
        return cls(
            intent=str(data.get("intent") or "knowledge_review"),
            confidence=float(data.get("confidence") or 0.0),
            years=[int(item) for item in clean_list(data.get("years")) if str(item).isdigit()],
            literal_filters=[str(item) for item in clean_list(data.get("literal_filters")) if str(item).strip()],
            requested_entities=[str(item) for item in clean_list(data.get("requested_entities")) if str(item).strip()],
            requested_metrics=[str(item) for item in clean_list(data.get("requested_metrics")) if str(item).strip()],
            requested_dimensions=[str(item) for item in clean_list(data.get("requested_dimensions")) if str(item).strip()],
            ambiguities=[str(item) for item in clean_list(data.get("ambiguities")) if str(item).strip()],
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class StageResult:
    name: str
    payload: dict
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Phase1Result:
    question: str
    intent_spec: dict
    business_spec: dict
    schema_plan: dict
    validation: dict
    context: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SqlArtifact:
    operation: str
    sql: str
    limit: int
    tables: list[str] = field(default_factory=list)
    joins: list[dict] = field(default_factory=list)
    filters: list[dict] = field(default_factory=list)
    metrics: list[dict] = field(default_factory=list)
    group_by: list[Any] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
