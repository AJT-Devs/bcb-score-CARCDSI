"""Formato textual local para resultados já calculados."""
from .briefing import generate_briefing


def report_from_metrics(metrics):
    return generate_briefing(metrics) + "\n"
