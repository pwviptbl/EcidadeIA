from __future__ import annotations

import json
from typing import Any

import requests

from agente_v2.config import MCP_SERVER_URL
from agente_v2.infrastructure.logger import log_event


class McpClient:
    def __init__(self, server_url: str = MCP_SERVER_URL, timeout: int = 60):
        self.server_url = server_url
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 1

    def health(self) -> dict:
        return self.call_tool("ecidade_health", {})

    def catalog_search(self, text: str, limit: int) -> dict:
        return self.call_tool("ecidade_catalog_search", {"text": text, "limit": limit})

    def rag_search(self, text: str, limit: int, kinds: list[str]) -> dict:
        return self.call_tool("ecidade_catalog_rag_search", {"text": text, "limit": limit, "kinds": kinds})

    def describe_table(self, full_table: str) -> dict:
        schema, table = full_table.split(".", 1)
        return self.call_tool("ecidade_describe_table", {"schema": schema, "table": table})

    def relationships(self, tables: list[str]) -> dict:
        return self.call_tool("ecidade_get_relationships", {"tables": tables})

    def readonly_query(self, sql: str, limit: int = 1000, statement_timeout_ms: int | None = None) -> dict:
        arguments: dict[str, Any] = {"sql": sql, "limit": limit}
        if statement_timeout_ms is not None:
            arguments["statement_timeout_ms"] = int(statement_timeout_ms)
        return self.call_tool("ecidade_readonly_query", arguments)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict:
        log_event("mcp.tool.start", {"tool": name, "arguments": arguments})
        self._ensure_session()
        response = self._rpc("tools/call", {"name": name, "arguments": arguments})
        result = response.get("result", {})
        if isinstance(result.get("structuredContent"), dict):
            final = result["structuredContent"]
            log_event("mcp.tool.done", {"tool": name, "result_keys": list(final.keys())})
            return final
        content = result.get("content") or []
        text = "".join(str(item.get("text") or "") for item in content if isinstance(item, dict)).strip()
        if text:
            if text.lower().startswith("error executing tool"):
                raise RuntimeError(text)
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return {"text": text}
            if isinstance(parsed, dict):
                log_event("mcp.tool.done", {"tool": name, "result_keys": list(parsed.keys())})
                return parsed
        return result if isinstance(result, dict) else {}

    def _ensure_session(self) -> None:
        if self.session_id:
            return
        self._rpc(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "agente-v2", "version": "0.1"},
            },
        )
        requests.post(
            self.server_url,
            headers=self._headers(),
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            timeout=self.timeout,
        )

    def _rpc(self, method: str, params: dict[str, Any], retry_session: bool = True) -> dict:
        request_id = self._next_id
        self._next_id += 1
        response = requests.post(
            self.server_url,
            headers=self._headers(),
            json={"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
            timeout=self.timeout,
        )
        if response.headers.get("mcp-session-id"):
            self.session_id = response.headers["mcp-session-id"]
        text = self._response_text(response)
        log_event("mcp.rpc", {"method": method, "status": response.status_code, "session": bool(self.session_id)})
        if response.status_code >= 400:
            if retry_session and response.status_code == 404 and "Session not found" in text and method != "initialize":
                self.session_id = None
                self._ensure_session()
                return self._rpc(method, params, retry_session=False)
            raise RuntimeError(f"MCP HTTP {response.status_code}: {text[:500]}")
        parsed = self._parse_response(text)
        if parsed.get("error"):
            raise RuntimeError(f"MCP error: {parsed['error']}")
        return parsed

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        return headers

    def _parse_response(self, text: str) -> dict:
        stripped = text.strip()
        if not stripped:
            return {}
        if stripped.startswith("{"):
            return json.loads(stripped)
        for line in stripped.splitlines():
            if line.startswith("data:"):
                data = line.split(":", 1)[1].strip()
                if data:
                    return json.loads(data)
        raise RuntimeError(f"Resposta MCP invalida: {text[:500]}")

    def _response_text(self, response: requests.Response) -> str:
        try:
            return response.content.decode("utf-8")
        except UnicodeDecodeError:
            return response.content.decode("utf-8", errors="replace")
