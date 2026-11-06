"""Validações estruturais mínimas antes do processamento."""

from collections.abc import Iterable

from config.constants import REQUIRED_COLUMNS


def validate_required_columns(columns: Iterable[str]) -> None:
    missing = sorted(set(REQUIRED_COLUMNS) - set(columns))
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")