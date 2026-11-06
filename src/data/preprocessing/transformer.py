"""Transformações numéricas do dataset."""

import pandas as pd


def add_credit_ratios(frame: pd.DataFrame) -> pd.DataFrame:
    transformed = frame.copy()
    active = transformed["carteira_ativa"].replace(0, pd.NA)
    transformed["proporcao_inadimplencia"] = transformed["carteira_inadimplencia"] / active
    transformed["proporcao_ativos_problematicos"] = transformed["ativo_problematico"] / active
    return transformed