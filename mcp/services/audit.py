from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from config import AUDIT_PATH, DATA_DIR


def write_audit(event: str, payload: dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "payload": payload,
    }
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, default=str) + "\n")
