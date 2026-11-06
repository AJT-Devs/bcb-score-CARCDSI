"""Operações de limpeza de dados."""

import pandas as pd


def drop_empty_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.dropna(how="all").copy()