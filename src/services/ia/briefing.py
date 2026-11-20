"""Construção de briefings a partir de métricas produzidas pelo ML."""

from typing import Any

from .client import GeminiClient, LLMClient, LLMResponse, NVIDIAClient
from .prompts import build_briefing_prompt


def generate_briefing(
    metrics: dict[str, Any], provider: str = "gemini", *, client: LLMClient | None = None
) -> LLMResponse:
    prompt = build_briefing_prompt(str(metrics))
    if client is None:
        providers = {"nvidia": NVIDIAClient, "gemini": GeminiClient}
        if provider not in providers:
            raise ValueError(f"Provedor LLM desconhecido: {provider}")
        client = providers[provider]()
    return client.generate(prompt)
