from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


def load_env(path: Path = BASE_DIR / ".env"):
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_env()

CATALOG_DIR = Path(os.getenv("MCP_CATALOG_DIR", ROOT_DIR / "catalog"))
KNOWLEDGE_DIR = Path(os.getenv("MCP_KNOWLEDGE_DIR", ROOT_DIR / "knowledge"))
RAG_DOCUMENTS_PATH = Path(os.getenv("MCP_RAG_DOCUMENTS_PATH", ROOT_DIR / "rag" / "catalog_documents.jsonl"))
DATA_DIR = Path(os.getenv("MCP_DATA_DIR", BASE_DIR / "data"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_DATABASE = os.getenv("DB_DATABASE", "")
DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

ALLOWED_SCHEMAS = [
    item.strip()
    for item in os.getenv("MCP_ALLOWED_SCHEMAS", "cadastro").split(",")
    if item.strip()
]
QUERY_LIMIT = int(os.getenv("MCP_QUERY_LIMIT", "1000"))
STATEMENT_TIMEOUT_MS = int(os.getenv("MCP_STATEMENT_TIMEOUT_MS", "5000"))
AUDIT_PATH = DATA_DIR / "consultas.jsonl"
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio")
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", "8010"))
MCP_ALLOWED_HOSTS = [
    item.strip()
    for item in os.getenv("MCP_ALLOWED_HOSTS", "127.0.0.1:*,localhost:*").split(",")
    if item.strip()
]
MCP_ALLOWED_ORIGINS = [
    item.strip()
    for item in os.getenv("MCP_ALLOWED_ORIGINS", "http://127.0.0.1:*,http://localhost:*").split(",")
    if item.strip()
]
MCP_DISABLE_DNS_REBINDING_PROTECTION = os.getenv(
    "MCP_DISABLE_DNS_REBINDING_PROTECTION",
    "false",
).lower() in ("1", "true", "yes", "on")
