"""Inferência em lote com CatBoost persistido e os mesmos atributos temporais."""
import argparse
import json
from pathlib import Path
import pandas as pd
from config.constants import PROFILE_COLUMNS, TARGET_DEFAULTS
from config.settings import DEFAULT_INTERIM
from data.read.monthly_files import file_month, monthly_files
from features.temporal import build_features
from models.catboost_regression import load_predict
from models.baselines import predict_baselines
from models.temporal_validation import SPLIT_FILE, load_origins


def predict(panel, model_dir, origin, methods=("catboost", "baselines")):
    unknown = set(methods) - {"baselines", "linear", "tree", "knn", "catboost"}
    if unknown:
        raise ValueError(f"Modelos desconhecidos: {sorted(unknown)}")
    if set(methods) - {"baselines"}:
        split = load_origins(model_dir)
        phase = "validation" if "catboost" in methods else "train"
        cutoff = str(pd.Period(max(split[phase]), freq="M") + 1)
        if origin < cutoff:
            raise ValueError(f"Os modelos usam rótulos até {cutoff}; origem anterior ao corte")
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
    p.add_argument("--interim", default=str(DEFAULT_INTERIM))
    p.add_argument("--models", required=True)
    p.add_argument("--origin", required=True)
    p.add_argument("--methods", default="catboost,baselines", help="baselines,linear,tree,knn,catboost")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    folder = Path(args.interim)
    if file_month(f"scrdata_{args.origin.replace('-', '')}.csv") != args.origin:
        p.error("--origin deve usar o formato AAAA-MM")
    start = str(pd.Period(args.origin, freq="M") - 2)
    files = dict(monthly_files(folder, start, args.origin))
    metadata = folder / SPLIT_FILE
    if metadata.is_file():
        panel_months = json.loads(metadata.read_text(encoding="utf-8")).get("panel_months", files)
        files = {month: path for month, path in files.items() if month in panel_months}
    if args.origin not in files:
        p.error(f"Mês de origem ausente em {folder} ({args.origin})")
    profile_types = dict.fromkeys(PROFILE_COLUMNS, str)
    panel = pd.concat([pd.read_csv(path, dtype=profile_types, keep_default_na=False, na_values=[""])
                       for path in files.values()], ignore_index=True)
    keys = pd.read_csv(folder / "profiles.csv", dtype=profile_types, keep_default_na=False)
    panel = panel.merge(keys, on=list(PROFILE_COLUMNS), validate="many_to_one")
    predict(panel, args.models, args.origin, args.methods.split(",")).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
