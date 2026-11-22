"""Métricas em proporção e pontos percentuais; cobertura explícita."""
import numpy as np
import pandas as pd


def metrics(y, pred):
    y, pred = np.asarray(y, dtype=float), np.asarray(pred, dtype=float)
    eligible = np.isfinite(y)
    valid = eligible & np.isfinite(pred)
    a, p = y[valid], pred[valid]
    error = p - a
    n = len(a)
    denominator = float(((a - a.mean()) ** 2).sum()) if n else 0
    mae = float(np.abs(error).mean()) if n else None
    rmse = float(np.sqrt((error ** 2).mean())) if n else None
    return {"n_eligible": int(eligible.sum()), "n": n,
            "n_predictions": int(np.isfinite(pred).sum()),
            "coverage": n / int(eligible.sum()) if eligible.any() else None,
            "mae": mae, "rmse": rmse, "mae_pp": 100 * mae if n else None,
            "rmse_pp": 100 * rmse if n else None,
            "r2": 1 - float((error ** 2).sum()) / denominator if n >= 2 and denominator > 0 else None,
            "out_of_range": int(((p < 0) | (p > 1)).sum()),
            "out_of_range_all": int((np.isfinite(pred) & ((pred < 0) | (pred > 1))).sum())}


def evaluate_table(frame, target, methods, masks):
    """Avalia o mesmo índice, incluindo interseção e recortes descritivos."""
    table = pd.DataFrame(methods, index=frame.index)
    common = np.isfinite(table).all(axis=1)
    y = frame[f"y_{target}"]
    rows = []
    for split in ("validation", "test"):
        for scope, restriction in (("available", np.ones(len(frame), dtype=bool)), ("common", common)):
            subset = masks[split] & restriction
            for model in table:
                rows.append({"split": split, "scope": scope, "target": target, "model": model,
                             **metrics(y[subset], table.loc[subset, model])})
        for group_col in ("month", "uf", "cliente", "segmento"):
            for group, part in frame.loc[masks[split] & common].groupby(group_col, observed=True):
                for model in table:
                    rows.append({"split": split, "scope": f"{group_col}={group}", "target": target,
                                 "model": model, **metrics(y.loc[part.index], table.loc[part.index, model])})
    return rows
