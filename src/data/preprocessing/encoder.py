"""Codificação de variáveis categóricas para modelagem."""

import pandas as pd


def encode_categories(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    encoded = frame.copy()
    for column in columns:
        if column in encoded:
            encoded[column] = encoded[column].astype("category").cat.codes
    return encoded