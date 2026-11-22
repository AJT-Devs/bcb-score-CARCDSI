"""Junções por calendário exato, sem preenchimento de meses ausentes."""
import pandas as pd
from config.constants import TARGET_DEFAULTS


def build_features(panel):
    if panel.duplicated(["series_id", "month"]).any():
        raise ValueError("Perfil/mês duplicado")
    result = panel.copy()
    result["target_month"] = (pd.PeriodIndex(result.month, freq="M") + 1).astype(str)
    labels = panel[["series_id", "month", *TARGET_DEFAULTS]].rename(columns={"month": "target_month", **{t: f"y_{t}" for t in TARGET_DEFAULTS}})
    result = result.merge(labels, on=["series_id", "target_month"], how="left", validate="one_to_one")
    for lag in (1, 2):
        history = panel[["series_id", "month", *TARGET_DEFAULTS]].copy()
        history["month"] = (pd.PeriodIndex(history.month, freq="M") + lag).astype(str)
        history = history.rename(columns={t: f"{t}_lag{lag}" for t in TARGET_DEFAULTS})
        result = result.merge(history, on=["series_id", "month"], how="left", validate="one_to_one")
    for t in TARGET_DEFAULTS:
        cols = [t, f"{t}_lag1", f"{t}_lag2"]
        result[f"{t}_mean3"] = result[cols].mean(axis=1).where(result[cols].notna().all(axis=1))
    result["month_number"] = pd.PeriodIndex(result.month, freq="M").month
    return result
