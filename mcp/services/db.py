from __future__ import annotations

import time
from decimal import Decimal
from typing import Any

import psycopg
from psycopg.rows import dict_row

from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USERNAME, STATEMENT_TIMEOUT_MS


class Database:
    def connect(self):
        return psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_DATABASE,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            row_factory=dict_row,
            connect_timeout=5,
        )

    def health(self) -> dict:
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("select current_database() as database, current_user as user")
                return dict(cursor.fetchone())

    def fetch_all(self, sql: str, params: tuple | None = None, statement_timeout_ms: int | None = None) -> dict:
        started = time.monotonic()
        timeout_ms = int(statement_timeout_ms or STATEMENT_TIMEOUT_MS)
        with self.connect() as conn:
            conn.execute("begin read only")
            conn.execute(f"set local statement_timeout = {timeout_ms}")
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                rows = [self._normalize_row(row) for row in cursor.fetchall()]
        return {
            "rows": rows,
            "row_count": len(rows),
            "duration_ms": int((time.monotonic() - started) * 1000),
        }

    def fetch_one(self, sql: str, params: tuple | None = None) -> dict:
        result = self.fetch_all(sql, params)
        rows = result["rows"]
        return rows[0] if rows else {}

    def _normalize_row(self, row: dict[str, Any]) -> dict[str, Any]:
        normalized = {}
        for key, value in row.items():
            if isinstance(value, Decimal):
                normalized[key] = float(value)
            elif hasattr(value, "isoformat"):
                normalized[key] = value.isoformat()
            else:
                normalized[key] = value
        return normalized
