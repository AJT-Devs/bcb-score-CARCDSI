"""Inferência em lote com CatBoost persistido e os mesmos atributos temporais."""
import argparse
from pathlib import Path
import pandas as pd
from config.constants import TARGET_DEFAULTS
from features.temporal import build_features
from models.catboost_regression import load_predict
from models.baselines import predict_baselines


def predict(panel, model_dir, origin, methods=("catboost", "baselines")):
    unknown = set(methods) - {"baselines", "linear", "tree", "knn", "catboost"}
    if unknown:
        raise ValueError(f"Modelos desconhecidos: {sorted(unknown)}")
    if set(methods) - {"baselines"} and origin < "2025-09":
        raise ValueError("Modelos treinados até setembro de 2025 não podem prever origens anteriores")
    # Retira o futuro mesmo quando o chamador entrega painel com meses posteriores.
    frame = build_features(panel.loc[panel.month <= origin])
    frame = frame.loc[frame.month.eq(origin)].reset_index(drop=True)
    output = frame[["series_id", "month", "target_month"]].copy()
    for target in TARGET_DEFAULTS:
        if "catboost" in methods:
            output[f"catboost_{target}"] = load_predict(frame, Path(model_dir) / f"{target}.cbm")
        if "baselines" in methods:
            for method, values in predict_baselines(frame, target).items():
                output[f"{method}_{target}"] = values
        from models.classical_regression import load_predict as load_classical
        for method in methods:
            if method in {"linear", "tree", "knn"}:
                output[f"{method}_{target}"] = load_classical(frame, Path(model_dir) / f"{method}_{target}.joblib")
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--interim", default="data/interim/2025")
    p.add_argument("--models", required=True)
    p.add_argument("--origin", required=True)
    p.add_argument("--methods", default="catboost,baselines", help="baselines,linear,tree,knn,catboost")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    folder = Path(args.interim)
    panel = pd.concat([pd.read_csv(f) for f in sorted(folder.glob("scrdata_2025??.csv"))], ignore_index=True)
    keys = pd.read_csv(folder / "profiles.csv")
    from config.constants import PROFILE_COLUMNS
    panel = panel.merge(keys, on=list(PROFILE_COLUMNS), validate="many_to_one")
    predict(panel, args.models, args.origin, args.methods.split(",")).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
