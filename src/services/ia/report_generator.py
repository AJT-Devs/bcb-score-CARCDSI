"""Geração de relatórios textuais a partir dos briefings."""

from .client import LLMResponse


def report_from_response(response: LLMResponse) -> str:
    return f"Provedor: {response.provider}\n\n{response.text.strip()}\n"