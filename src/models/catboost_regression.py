"""Dois regressores independentes: rótulos ausentes não eliminam o outro alvo."""
import json
from pathlib import Path
import numpy as np
from config.constants import PROFILE_COLUMNS, TARGET_DEFAULTS, BALANCE_COLUMNS
from models.evaluation import metrics


def feature_columns():
    return [*PROFILE_COLUMNS, *BALANCE_COLUMNS, "month_number", *TARGET_DEFAULTS,
            *[f"{t}_{suffix}" for t in TARGET_DEFAULTS for suffix in ("lag1", "lag2", "mean3")]]


def model_inputs(frame):
    x = frame[feature_columns()].copy()
    for col in PROFILE_COLUMNS:
        x[col] = x[col].fillna("__MISSING__").astype(str)
    return x.replace([np.inf, -np.inf], np.nan)


def train_target(frame, masks, target, output: Path):
    from catboost import CatBoostRegressor
    x, y = model_inputs(frame), frame[f"y_{target}"]
    train = masks["train"] & y.notna()
    val = masks["validation"] & y.notna()
    if not train.any() or not val.any():
        raise ValueError("Treino/validação sem rótulos")
    candidates, best, score = [], None, float("inf")
    for depth in (4, 6):
        config = dict(iterations=200, depth=depth, learning_rate=0.05, loss_function="MAE",
                      random_seed=42, thread_count=4, verbose=False, allow_writing_files=False,
                      nan_mode="Min")
        model = CatBoostRegressor(**config)
        model.fit(x.loc[train], y.loc[train], cat_features=list(PROFILE_COLUMNS))
        result = metrics(y.loc[val], model.predict(x.loc[val]))
        candidates.append({"config": config, "validation": result})
        if result["mae"] < score:
            best, score = model, result["mae"]
    output.mkdir(parents=True, exist_ok=True)
    best.save_model(str(output / f"{target}.cbm"))
    (output / f"{target}.json").write_text(json.dumps({"candidates": candidates, "selected": best.get_params(),
        "features": feature_columns(), "training_rows": int(train.sum()), "refit": False}, indent=2), encoding="utf-8")
    # Não refaz ajuste com novembro: o modelo congelado mantém o protocolo comum.
    return best.predict(x), candidates


def load_predict(frame, model_path):
    from catboost import CatBoostRegressor
    model = CatBoostRegressor()
    model.load_model(str(model_path))
    return model.predict(model_inputs(frame))
