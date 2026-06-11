from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from config import DATA_DIR


LOG_PATH = DATA_DIR / "agente.log"


def log_event(event: str, payload: dict[str, Any] | None = None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "payload": _compact(payload or {}),
    }
    line = json.dumps(record, ensure_ascii=False, default=str)
    print(f"[agente] {line}", flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def _compact(value):
    if isinstance(value, dict):
        return {str(key): _compact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_compact(item) for item in value[:20]]
    if isinstance(value, str):
        return value if len(value) <= 1200 else value[:1200] + "...[truncated]"
    return value
