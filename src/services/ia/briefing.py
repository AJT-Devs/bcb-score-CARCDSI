"""Representação legível de métricas previamente calculadas."""
import json


def generate_briefing(metrics):
    return json.dumps(metrics, ensure_ascii=False, indent=2, allow_nan=False)
