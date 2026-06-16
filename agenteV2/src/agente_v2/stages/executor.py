from __future__ import annotations

import os
from typing import Any

from agente_v2.contracts.models import ExecutionArtifact, SqlArtifact
from agente_v2.infrastructure.logger import log_event
from agente_v2.infrastructure.mcp import McpClient


class Executor:
    def __init__(self, mcp: McpClient | None = None):
        self.mcp = mcp or McpClient()

    def run(self, artifact: SqlArtifact, sql: str | None = None, limit: int | None = None) -> ExecutionArtifact:
        final_sql = str(sql or artifact.sql or "").strip().rstrip(";")
        final_limit = int(limit or artifact.limit or 1000)
        statement_timeout_ms = self._execution_timeout_ms(artifact)
        try:
            payload = self.mcp.readonly_query(final_sql, limit=final_limit, statement_timeout_ms=statement_timeout_ms)
            result = ExecutionArtifact(
                ok=True,
                sql=final_sql,
                limit=int(payload.get("limit") or final_limit),
                row_count=int(payload.get("row_count") or 0),
                duration_ms=int(payload.get("duration_ms") or 0),
                rows=payload.get("rows") if isinstance(payload.get("rows"), list) else [],
                notes=["Consulta executada via MCP read-only."],
            )
        except Exception as exc:
            result = ExecutionArtifact(
                ok=False,
                sql=final_sql,
                limit=final_limit,
                error=str(exc),
                notes=["Falha ao executar consulta read-only."],
            )
        log_event("executor.done", result.to_dict())
        return result

    def _execution_timeout_ms(self, artifact: SqlArtifact) -> int:
        default_timeout = int(os.getenv("AGENTEV2_EXECUTION_TIMEOUT_MS", "15000"))
        compare_timeout = int(os.getenv("AGENTEV2_COMPARE_PERIODS_TIMEOUT_MS", "30000"))
        if artifact.operation == "compare_periods":
            return compare_timeout
        if artifact.operation in {"count_by_dimension", "sum_by_dimension"} and len(artifact.joins) > 1:
            return max(default_timeout, compare_timeout // 2)
        return default_timeout
