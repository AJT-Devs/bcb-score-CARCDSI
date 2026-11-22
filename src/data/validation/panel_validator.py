"""Integridade de calendário, granularidade e perfis do painel mensal."""
from config.constants import PROFILE_COLUMNS


def validate_month(frame, expected, filename):
    if not frame["month"].eq(expected).all():
        raise ValueError(f"Mês incompatível: {filename}")


def valid_profile_mask(frame):
    if frame[list(PROFILE_COLUMNS)].apply(
        lambda s: s.str.casefold().isin(["total", "todos", "todas"])
    ).any().any():
        raise ValueError("Nível de total encontrado; revisão de granularidade necessária")
    return ~frame[list(PROFILE_COLUMNS)].eq("").any(axis=1)


def validate_unique_keys(frame, filename):
    if frame.duplicated([*PROFILE_COLUMNS, "month"]).any():
        raise ValueError(f"Chave duplicada em {filename}; não somar duplicatas silenciosamente")
