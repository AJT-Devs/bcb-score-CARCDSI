"""Transformações numéricas do dataset."""

import pandas as pd
import numpy as np


def add_credit_ratios(frame: pd.DataFrame) -> pd.DataFrame:
    transformed = frame.copy()
    active = pd.to_numeric(transformed["carteira_ativa"], errors="coerce")
    active = active.where(np.isfinite(active) & (active > 0))
    for target, balance in zip(("proporcao_inadimplencia", "proporcao_ativos_problematicos"), ("carteira_inadimplencia", "ativo_problematico")):
        value = pd.to_numeric(transformed[balance], errors="coerce")
        transformed[target] = (value / active).where(np.isfinite(value) & (value >= 0) & (value <= active))
    return transformed
