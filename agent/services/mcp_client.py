from __future__ import annotations

import json
from typing import Any

import requests

from config import MCP_SERVER_URL
from services.logger import log_event


class McpClient:
    def __init__(self, server_url: str = MCP_SERVER_URL, timeout: int = 60):
        self.server_url = server_url
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 1

    def health(self) -> dict:
        return self.call_tool("ecidade_health", {})

    def catalog_index(self) -> dict:
        return self.call_tool("ecidade_catalog_index", {})

    def schemas(self) -> dict:
        return self.call_tool("ecidade_list_schemas", {})

    def tables(self, schema: str = "cadastro") -> dict:
        return self.call_tool("ecidade_list_tables", {"schema": schema})

    def table(self, schema: str, table: str) -> dict:
        return self.call_tool("ecidade_describe_table", {"schema": schema, "table": table})

    def relationships(self, tables: list[str] | None = None) -> dict:
        return self.call_tool("ecidade_get_relationships", {"tables": tables or []})

    def search_docs(self, term: str) -> dict:
        payload = self.call_tool("ecidade_catalog_search", {"text": term, "limit": 20})
        return {"results": payload.get("results", [])}

    def search_rag_docs(self, term: str, limit: int = 20, kinds: list[str] | None = None) -> dict:
        payload = self.call_tool(
            "ecidade_catalog_rag_search",
            {"text": term, "limit": limit, "kinds": kinds or []},
        )
        return {"results": payload.get("results", []), "loaded": payload.get("loaded", False)}

    def readonly_query(self, sql: str, limit: int = 1000) -> dict:
        return self.call_tool("ecidade_readonly_query", {"sql": sql, "limit": limit})

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict:
        log_event("mcp.tool.start", {"tool": name, "arguments": arguments})
        self._ensure_session()
        response = self._rpc(
            "tools/call",
            {
                "name": name,
                "arguments": arguments,
            },
        )
        result = response.get("result", {})
        if "structuredContent" in result and isinstance(result["structuredContent"], dict):
            final = result["structuredContent"]
            log_event("mcp.tool.done", {"tool": name, "result_keys": list(final.keys())})
            return final

        content = result.get("content") or []
        if content and isinstance(content, list):
            text = "".join(str(item.get("text", "")) for item in content if isinstance(item, dict)).strip()
            if text:
                if text.lower().startswith("error executing tool"):
                    raise RuntimeError(text)
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, dict):
                        log_event("mcp.tool.done", {"tool": name, "result_keys": list(parsed.keys())})
                        return parsed
                except json.JSONDecodeError:
                    log_event("mcp.tool.done", {"tool": name, "text": text})
                    return {"text": text}
        final = result if isinstance(result, dict) else {}
        log_event("mcp.tool.done", {"tool": name, "result_keys": list(final.keys())})
        return final

    def _ensure_session(self):
        if self.session_id:
            return
        self._rpc(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "agente-externo", "version": "0.1"},
            },
        )
        self._notify_initialized()

    def _notify_initialized(self):
        headers = self._headers()
        requests.post(
            self.server_url,
            headers=headers,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            timeout=self.timeout,
        )

    def _rpc(self, method: str, params: dict[str, Any], retry_session: bool = True) -> dict:
        request_id = self._next_id
        self._next_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }
        response = requests.post(self.server_url, headers=self._headers(), json=payload, timeout=self.timeout)
        log_event("mcp.rpc", {"method": method, "status": response.status_code, "session": bool(self.session_id)})
        if response.headers.get("mcp-session-id"):
            self.session_id = response.headers["mcp-session-id"]
        response_text = self._response_text(response)
        if response.status_code >= 400:
            if (
                retry_session
                and response.status_code == 404
                and "Session not found" in response_text
                and method != "initialize"
            ):
                self.session_id = None
                self._ensure_session()
                return self._rpc(method, params, retry_session=False)
            raise RuntimeError(f"MCP HTTP {response.status_code}: {response_text[:500]}")
        parsed = self._parse_response(response_text)
        if parsed.get("error"):
            raise RuntimeError(f"MCP error: {parsed['error']}")
        return parsed

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
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
        content_type = str(response.headers.get("content-type") or "").lower()
        if "application/json" in content_type or "text/event-stream" in content_type:
            try:
                return response.content.decode("utf-8")
            except UnicodeDecodeError:
                return response.content.decode("utf-8", errors="replace")
        return response.text
