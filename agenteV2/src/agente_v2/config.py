from __future__ import annotations

import os
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[3]
AGENTEV2_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = AGENTEV2_DIR / "data"


def _load_env_file(path: Path, override: bool = False) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


_load_env_file(REPO_DIR / ".env", override=False)
_load_env_file(AGENTEV2_DIR / ".env", override=True)

MCP_SERVER_URL = os.getenv("AGENTEV2_MCP_SERVER_URL", os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8010/mcp")).rstrip("/")

LLM_PROVIDER = os.getenv("AGENTEV2_LLM_PROVIDER", "gemini")
PLANNER_MODEL = os.getenv("AGENTEV2_PLANNER_MODEL", "gemini-2.5-flash")
LIGHT_MODEL = os.getenv("AGENTEV2_LIGHT_MODEL", "gemini-3.1-flash-lite")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com").rstrip("/")
GEMINI_TIMEOUT = int(os.getenv("AGENTEV2_GEMINI_TIMEOUT", os.getenv("GEMINI_TIMEOUT", "120")))

DEFAULT_SCHEMA = os.getenv("AGENTEV2_DEFAULT_SCHEMA", "cadastro")
RAG_LIMIT = int(os.getenv("AGENTEV2_RAG_LIMIT", "16"))
CATALOG_SEARCH_LIMIT = int(os.getenv("AGENTEV2_CATALOG_SEARCH_LIMIT", "12"))
