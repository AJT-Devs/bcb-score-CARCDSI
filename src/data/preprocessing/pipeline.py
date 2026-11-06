"""Orquestração do pré-processamento inicial."""

import pandas as pd

from .cleaner import drop_empty_rows
from .transformer import add_credit_ratios


def preprocess(frame: pd.DataFrame) -> pd.DataFrame:
    return add_credit_ratios(drop_empty_rows(frame))