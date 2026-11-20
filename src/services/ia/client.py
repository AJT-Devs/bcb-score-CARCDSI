"""Clientes REST mínimos para NVIDIA NIM e Google Gemini."""

import json
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.settings import get_settings


@dataclass(frozen=True)
class LLMResponse:
    provider: str
    text: str
    raw: dict[str, Any]


class LLMClient(Protocol):
    """Contrato para qualquer cliente que interprete um prompt de texto."""

    def generate(self, prompt: str) -> LLMResponse: ...


class LLMRequestError(RuntimeError):
    """Erro normalizado de comunicação com um provedor LLM."""


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as error:
        raise LLMRequestError(f"Falha na requisição ao LLM: {error}") from error


class NVIDIAClient:
    endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.nvidia_api_key
        self.model = model or settings.nvidia_model
        self.timeout = settings.request_timeout_seconds

    def generate(self, prompt: str) -> LLMResponse:
        if not self.api_key:
            raise LLMRequestError("NVIDIA_API_KEY não está configurada")
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        raw = _post_json(self.endpoint, {"Authorization": f"Bearer {self.api_key}"}, payload, self.timeout)
        return LLMResponse("nvidia", raw["choices"][0]["message"]["content"], raw)


class GeminiClient:
    endpoint_template = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        self.timeout = settings.request_timeout_seconds

    def generate(self, prompt: str) -> LLMResponse:
        if not self.api_key:
            raise LLMRequestError("GEMINI_API_KEY não está configurada")
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        endpoint = self.endpoint_template.format(model=self.model)
        raw = _post_json(endpoint, {"x-goog-api-key": self.api_key}, payload, self.timeout)
        text = raw["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResponse("gemini", text, raw)
