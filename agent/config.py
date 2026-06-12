import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def _load_env_file(path: Path, override: bool = True):
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


_load_env_file(BASE_DIR / ".env", override=True)

CATALOG_DIR = Path(os.getenv("AGENTE_CATALOG_DIR", BASE_DIR.parent / "catalog"))

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8010/mcp").rstrip("/")

AGENTE_LLM_PROVIDER = os.getenv("AGENTE_LLM_PROVIDER", "ollama")
AGENTE_LLM_MODEL = os.getenv("AGENTE_LLM_MODEL", "qwen2.5-coder:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://192.168.1.19:11434").rstrip("/")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "900"))
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "2048"))
OLLAMA_NUM_PREDICT = int(os.getenv("OLLAMA_NUM_PREDICT", "1024"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com").rstrip("/")
GEMINI_TIMEOUT = int(os.getenv("GEMINI_TIMEOUT", "120"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
AGENTE_PLANNER_LLM_PROVIDER = os.getenv("AGENTE_PLANNER_LLM_PROVIDER", AGENTE_LLM_PROVIDER)
AGENTE_PLANNER_LLM_MODEL = os.getenv(
    "AGENTE_PLANNER_LLM_MODEL",
    GEMINI_MODEL if AGENTE_PLANNER_LLM_PROVIDER == "gemini" else AGENTE_LLM_MODEL,
)
AGENTE_ANSWER_LLM_PROVIDER = os.getenv("AGENTE_ANSWER_LLM_PROVIDER", AGENTE_LLM_PROVIDER)
AGENTE_ANSWER_LLM_MODEL = os.getenv(
    "AGENTE_ANSWER_LLM_MODEL",
    GEMINI_MODEL if AGENTE_ANSWER_LLM_PROVIDER == "gemini" else AGENTE_LLM_MODEL,
)

AGENTE_HOST = os.getenv("AGENTE_HOST", "127.0.0.1")
AGENTE_PORT = int(os.getenv("AGENTE_PORT", "5055"))
AGENTE_DEBUG = os.getenv("AGENTE_DEBUG", "false").lower() in ("1", "true", "yes", "on")
AGENTE_VALIDATE_RESULTS = os.getenv("AGENTE_VALIDATE_RESULTS", "false").lower() in ("1", "true", "yes", "on")
AGENTE_STOP_AFTER_STAGE = str(os.getenv("AGENTE_STOP_AFTER_STAGE", "")).strip().lower()

DATABASE_PATH = DATA_DIR / "chat.sqlite3"
DEFAULT_LIMIT = int(os.getenv("AGENTE_QUERY_LIMIT", "1000"))
