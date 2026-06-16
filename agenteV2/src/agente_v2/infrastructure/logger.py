from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def log_event(event: str, payload: dict[str, Any] | None = None) -> None:
    record = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "payload": _compact(payload or {}),
    }
    print("[agenteV2] " + json.dumps(record, ensure_ascii=False, default=str), flush=True)


def _compact(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _compact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_compact(item) for item in value[:20]]
    if isinstance(value, str):
        return value if len(value) <= 1200 else value[:1200] + "...[truncated]"
    return value
