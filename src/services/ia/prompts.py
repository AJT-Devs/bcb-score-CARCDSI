"""Templates de prompts para interpretação de resultados."""

BRIEFING_PROMPT = """Você é um analista de risco de crédito.
Interprete exclusivamente as métricas fornecidas abaixo, sem inventar valores.
Apresente achados, limitações e recomendações em linguagem objetiva.

Métricas:
{metrics}
"""


def build_briefing_prompt(metrics: str) -> str:
    return BRIEFING_PROMPT.format(metrics=metrics)