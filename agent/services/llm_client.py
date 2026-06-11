from __future__ import annotations

import json
import re
from typing import Any

import requests

from config import (
    AGENTE_LLM_MODEL,
    AGENTE_LLM_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_BASE_URL,
    GEMINI_TIMEOUT,
    OLLAMA_BASE_URL,
    OLLAMA_NUM_CTX,
    OLLAMA_NUM_PREDICT,
    OLLAMA_TIMEOUT,
)
from services.logger import log_event


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, provider: str = AGENTE_LLM_PROVIDER, model: str = AGENTE_LLM_MODEL):
        self.provider = provider
        self.model = model

    def json(self, system: str, user: str, num_predict: int | None = None) -> dict:
        text = self.text(system, user, num_predict=num_predict, json_mode=True)
        return self._parse_json(text)

    def text(self, system: str, user: str, num_predict: int | None = None, json_mode: bool = False) -> str:
        if self.provider == "ollama":
            return self._ollama(system, user, num_predict=num_predict, json_mode=json_mode)
        if self.provider == "gemini":
            return self._gemini(system, user)
        raise LLMError(f"Provider nao suportado no MVP: {self.provider}")

    def _ollama(self, system: str, user: str, num_predict: int | None = None, json_mode: bool = False) -> str:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        effective_num_predict = int(num_predict or OLLAMA_NUM_PREDICT)
        payload = {
            "model": self.model,
            "system": system,
            "prompt": user,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": OLLAMA_NUM_CTX,
                "num_predict": effective_num_predict,
            },
        }
        if json_mode:
            payload["format"] = "json"
        prompt_bytes = len(json.dumps({"system": system, "prompt": user}, ensure_ascii=False))
        log_event(
            "llm.request",
            {
                "provider": self.provider,
                "model": self.model,
                "url": url,
                "prompt_bytes": prompt_bytes,
                "num_ctx": OLLAMA_NUM_CTX,
                "num_predict": effective_num_predict,
                "timeout": OLLAMA_TIMEOUT,
                "prompt_preview": user[:1200],
            },
        )

        try:
            response = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
        except requests.RequestException as exc:
            raise LLMError(f"Falha de rede ao chamar Ollama: {self._sanitize(str(exc))}") from exc

        if response.status_code >= 400:
            detail = self._sanitize(response.text[:500])
            raise LLMError(f"Ollama HTTP {response.status_code}: {detail}")

        data = response.json()
        text = str(data.get("response") or "").strip()
        log_event(
            "llm.response",
            {
                "model": self.model,
                "response_bytes": len(text.encode("utf-8")),
                "total_duration": data.get("total_duration"),
                "load_duration": data.get("load_duration"),
                "prompt_eval_count": data.get("prompt_eval_count"),
                "prompt_eval_duration": data.get("prompt_eval_duration"),
                "eval_count": data.get("eval_count"),
                "eval_duration": data.get("eval_duration"),
            },
        )
        if not text:
            raise LLMError("Ollama retornou resposta vazia.")

        return text

    def _gemini(self, system: str, user: str) -> str:
        if not GEMINI_API_KEY:
            raise LLMError("GEMINI_API_KEY nao configurada.")

        url = f"{GEMINI_BASE_URL}/v1beta/models/{self.model}:generateContent"
        payload = {
            "system_instruction": {
                "parts": [{"text": system}],
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user}],
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json",
            },
        }
        prompt_bytes = len(json.dumps({"system": system, "prompt": user}, ensure_ascii=False))
        log_event(
            "llm.request",
            {
                "provider": self.provider,
                "model": self.model,
                "url": f"{url}?key=***",
                "prompt_bytes": prompt_bytes,
                "timeout": GEMINI_TIMEOUT,
                "prompt_preview": user[:1200],
            },
        )

        try:
            response = requests.post(
                url,
                params={"key": GEMINI_API_KEY},
                json=payload,
                timeout=GEMINI_TIMEOUT,
            )
        except requests.RequestException as exc:
            raise LLMError(f"Falha de rede ao chamar Gemini: {self._sanitize(str(exc))}") from exc

        if response.status_code >= 400:
            detail = self._sanitize(response.text[:500])
            raise LLMError(f"Gemini HTTP {response.status_code}: {detail}")

        data = response.json()
        text = self._extract_gemini_text(data)
        log_event(
            "llm.response",
            {
                "provider": self.provider,
                "model": self.model,
                "response_bytes": len(text.encode("utf-8")),
                "usage_metadata": data.get("usageMetadata"),
            },
        )
        if not text:
            raise LLMError("Gemini retornou resposta vazia.")

        return text

    def _extract_gemini_text(self, data: dict) -> str:
        try:
            parts = data["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Gemini retornou payload inesperado: {self._sanitize(json.dumps(data)[:500])}") from exc

        texts = [str(part.get("text") or "") for part in parts if isinstance(part, dict)]
        return "\n".join(text for text in texts if text).strip()

    def _parse_json(self, text: str) -> dict:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            parsed: Any = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            if self._looks_truncated(cleaned):
                raise LLMError(
                    "Resposta da IA parece ter sido cortada antes de fechar o JSON. "
                    "Aumente OLLAMA_NUM_PREDICT ou reduza o contexto enviado ao modelo."
                ) from exc
            match = re.search(r"\{.*\}", cleaned, flags=re.S)
            if not match:
                raise LLMError(f"Resposta da IA nao e JSON valido: {cleaned[:500]}") from exc
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError as nested_exc:
                raise LLMError(f"Resposta da IA nao e JSON valido: {cleaned[:500]}") from nested_exc

        if not isinstance(parsed, dict):
            raise LLMError("Resposta da IA deve ser um objeto JSON.")
        return parsed

    def _looks_truncated(self, value: str) -> bool:
        if not value:
            return False

        opened = value.count("{") + value.count("[")
        closed = value.count("}") + value.count("]")
        return value.startswith("{") and opened > closed

    def _sanitize(self, value: str) -> str:
        if not value:
            return value

        sanitized = re.sub(r"(OLLAMA_BASE_URL=)[^\\s]+", r"\1***", value)
        sanitized = re.sub(r"(key=)[^&\\s]+", r"\1***", sanitized)
        if GEMINI_API_KEY:
            sanitized = sanitized.replace(GEMINI_API_KEY, "***")
        return sanitized
