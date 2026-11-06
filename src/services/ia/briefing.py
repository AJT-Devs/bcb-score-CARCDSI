"""Construção de briefings a partir de métricas produzidas pelo ML."""

from typing import Any

from .client import GeminiClient, LLMResponse, NVIDIAClient
from .prompts import build_briefing_prompt


def generate_briefing(metrics: dict[str, Any], provider: str = "gemini") -> LLMResponse:
    prompt = build_briefing_prompt(str(metrics))
    client = NVIDIAClient() if provider == "nvidia" else GeminiClient()
    return client.generate(prompt)