"""Divisão cronológica por pares de meses consecutivos."""
import json
from pathlib import Path

import pandas as pd


SPLIT_FILE = "split-origins.json"
LEGACY_SPLIT = {"train": [f"2025-{month:02}" for month in range(1, 9)],
                "validation": ["2025-09", "2025-10"], "test": ["2025-11"]}


def split_origins(months):
    observed = set(months)
    origins = [month for month in sorted(observed)
               if str(pd.Period(month, freq="M") + 1) in observed]
    if len(origins) < 4:
        raise ValueError("São necessários ao menos quatro pares de meses consecutivos para treino, validação e teste")
    return {"train": origins[:-3], "validation": origins[-3:-1], "test": origins[-1:]}


def split_masks(frame, origins=None):
    if origins is None:
        origins = split_origins(frame.month.unique())
    return {name: frame.month.isin(months) for name, months in origins.items()}


def load_origins(folder):
    path = Path(folder) / SPLIT_FILE
    if not path.is_file():
        return LEGACY_SPLIT
    metadata = json.loads(path.read_text(encoding="utf-8"))
    return {phase: metadata[phase] for phase in LEGACY_SPLIT}
