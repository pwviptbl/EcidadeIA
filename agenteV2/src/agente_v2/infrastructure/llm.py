from __future__ import annotations

import json
import re
from typing import Any

import requests

from agente_v2.config import GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_TIMEOUT, LLM_PROVIDER, PLANNER_MODEL
from agente_v2.infrastructure.logger import log_event


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, provider: str = LLM_PROVIDER, model: str = PLANNER_MODEL, temperature: float = 0.1):
        self.provider = provider
        self.model = model
        self.temperature = temperature

    def json(self, system: str, user: dict[str, Any] | str) -> dict:
        text = self.text(system, user, json_mode=True)
        return self._parse_json(text)

    def text(self, system: str, user: dict[str, Any] | str, json_mode: bool = False) -> str:
        if self.provider != "gemini":
            raise LLMError(f"Provider nao suportado na V2 fase 1: {self.provider}")
        return self._gemini(system, user, json_mode=json_mode)

    def _gemini(self, system: str, user: dict[str, Any] | str, json_mode: bool) -> str:
        if not GEMINI_API_KEY:
            raise LLMError("GEMINI_API_KEY nao configurada.")

        prompt = user if isinstance(user, str) else json.dumps(user, ensure_ascii=False)
        url = f"{GEMINI_BASE_URL}/v1beta/models/{self.model}:generateContent"
        generation_config: dict[str, Any] = {"temperature": self.temperature}
        if json_mode:
            generation_config["response_mime_type"] = "application/json"
        payload = {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }
        log_event(
            "llm.request",
            {
                "provider": self.provider,
                "model": self.model,
                "url": f"{url}?key=***",
                "prompt_bytes": len(json.dumps({"system": system, "prompt": prompt}, ensure_ascii=False)),
            },
        )
        try:
            response = requests.post(url, params={"key": GEMINI_API_KEY}, json=payload, timeout=GEMINI_TIMEOUT)
        except requests.RequestException as exc:
            raise LLMError(f"Falha de rede ao chamar Gemini: {self._sanitize(str(exc))}") from exc
        if response.status_code >= 400:
            raise LLMError(f"Gemini HTTP {response.status_code}: {self._sanitize(response.text[:500])}")
        data = response.json()
        text = self._extract_text(data)
        log_event("llm.response", {"model": self.model, "response_bytes": len(text.encode("utf-8")), "usage": data.get("usageMetadata")})
        if not text:
            raise LLMError("Gemini retornou resposta vazia.")
        return text

    def _extract_text(self, data: dict) -> str:
        try:
            parts = data["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Gemini retornou payload inesperado: {self._sanitize(json.dumps(data)[:500])}") from exc
        return "\n".join(str(part.get("text") or "") for part in parts if isinstance(part, dict)).strip()

    def _parse_json(self, text: str) -> dict:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            match = re.search(r"\{.*\}", cleaned, flags=re.S)
            if not match:
                raise LLMError(f"Resposta da IA nao e JSON valido: {cleaned[:500]}") from exc
            parsed = json.loads(match.group(0))
        if not isinstance(parsed, dict):
            raise LLMError("Resposta da IA deve ser objeto JSON.")
        return parsed

    def _sanitize(self, value: str) -> str:
        if not value:
            return value
        sanitized = re.sub(r"(key=)[^&\\s]+", r"\1***", value)
        if GEMINI_API_KEY:
            sanitized = sanitized.replace(GEMINI_API_KEY, "***")
        return sanitized
