"""CLI reproduzível de preparação e experimento. Não chama serviços LLM."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import time
import hashlib
import numpy as np
import pandas as pd
from config.constants import TARGET_DEFAULTS, PROFILE_COLUMNS
from config.settings import DEFAULT_INTERIM, get_settings
from data.read.monthly_files import file_month
from data.read.panel import load_panel
from features.temporal import build_features
from models.temporal_validation import SPLIT_FILE, split_masks, split_origins
from models.baselines import predict_baselines
from models.evaluation import evaluate_table


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def run(args):
    start = time.perf_counter()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
                "platform": platform.platform(), "arguments": vars(args), "models": {},
                "versions": {p: importlib.metadata.version(p) for p in ("pandas", "numpy", "scikit-learn")},
                "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                "git_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()),
                "availability": "Avaliação por data-base e snapshot local; publicações históricas não reconstruídas; atraso oficial de cerca de 30 dias; possível otimismo operacional.",
                "source": "https://dadosabertos.bcb.gov.br/dataset/scr_data",
                "extraction_date": "Desconhecida; mtime não equivale à extração",
                "postprocessing": "Nenhum clipping", "fine_tuning": "Não executado"}
    manifest["source_hashes"] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(Path("src").rglob("*.py"))}
    manifest["environment"] = subprocess.check_output(
        [__import__("sys").executable, "-m", "pip", "freeze"], text=True).splitlines()
    write_json(output / "manifest.json", manifest)
    start_month, end_month = getattr(args, "start_month", None), getattr(args, "end_month", None)
    panel, audit, categories = load_panel(Path(args.raw), Path(args.interim), start_month, end_month)
    write_json(output / "data_audit.json", audit)
    write_json(output / "categories.json", categories)
    frame = build_features(panel)
    write_json(output / "temporal_audit.json", {
        str(month): {"rows": len(part), "profiles": int(part.series_id.nunique()),
                     "missing_next_target": {t: int(part[f"y_{t}"].isna().sum()) for t in TARGET_DEFAULTS},
                     "missing_three_month_context": {t: int(part[f"{t}_mean3"].isna().sum()) for t in TARGET_DEFAULTS}}
        for month, part in frame.groupby("month")})
    frame.to_csv(Path(args.interim) / "supervised.csv", index=False)
    panel_months = sorted(frame.month.unique())
    origins = split_origins(panel_months)
    write_json(Path(args.interim) / SPLIT_FILE, {**origins, "panel_months": panel_months})
    masks = split_masks(frame, origins)
    manifest["split"] = {name: {"origins": sorted(frame.loc[mask, "month"].unique()),
                                "targets": sorted(frame.loc[mask, "target_month"].unique()),
                                "rows": int(mask.sum()),
                                "valid_labels": {t: int(frame.loc[mask, f"y_{t}"].notna().sum()) for t in TARGET_DEFAULTS}}
                         for name, mask in masks.items()}
    write_json(output / "manifest.json", manifest)
    selected = args.models.split(",")
    allowed = {"baselines", "linear", "tree", "knn", "catboost", "chronos"}
    unknown = set(selected) - allowed
    if unknown:
        raise ValueError(f"Modelos desconhecidos: {sorted(unknown)}")
    if set(selected) & {"linear", "tree", "knn", "catboost"}:
        model_dir = output / "models"
        model_dir.mkdir()
        write_json(model_dir / SPLIT_FILE, origins)
    baseline_start = time.perf_counter()
    predictions = {t: predict_baselines(frame, t) if "baselines" in selected else {} for t in TARGET_DEFAULTS}
    if "baselines" in selected:
        manifest["models"]["baselines"] = {"status": "executed", "seconds": time.perf_counter() - baseline_start}
    evaluate = masks["validation"] | masks["test"]
    for method in selected:
        tick = time.perf_counter()
        try:
            if method in {"linear", "tree", "knn"}:
                from models.classical_regression import train_target
                for target in TARGET_DEFAULTS:
                    predictions[target][method], _ = train_target(frame, masks, target, output / "models", method, getattr(args, "knn_max_train", 5000), evaluate)
            elif method == "catboost":
                from models.catboost_regression import train_target
                for target in TARGET_DEFAULTS:
                    predictions[target][method], _ = train_target(frame, masks, target, output / "models")
                manifest["versions"][method] = importlib.metadata.version("catboost")
            elif method == "chronos":
                from models.chronos_forecast import ChronosForecaster, pilot_mask
                import torch
                torch.set_num_threads(4)
                checkpoint = ".tools/chronos-2" if Path(".tools/chronos-2/model.safetensors").exists() else "amazon/chronos-2"
                model = ChronosForecaster(checkpoint=checkpoint, revision=args.revision, device=args.device)
                sample = pilot_mask(frame, modulus=args.chronos_sample_modulus)
                manifest["chronos_sample"] = f"SHA256(JSON UTF8 da chave completa) módulo {args.chronos_sample_modulus} = 0; piloto CPU, sem seleção pelo target"
                for target in TARGET_DEFAULTS:
                    predictions[target][method] = model.predict_target(frame, target, evaluate & sample)
                manifest["versions"][method] = importlib.metadata.version("chronos-forecasting")
            elif method == "baselines":
                continue
            else:
                raise ValueError(f"Modelo desconhecido: {method}")
            manifest["models"][method] = {"status": "executed", "seconds": time.perf_counter() - tick}
        except (ImportError, OSError, RuntimeError, ValueError) as error:
            for target in TARGET_DEFAULTS:
                predictions[target].pop(method, None)
            manifest["models"][method] = {"status": "blocked", "error": str(error), "seconds": time.perf_counter() - tick}
        write_json(output / "manifest.json", manifest)
    rows, prediction_tables = [], []
    for target, methods in predictions.items():
        table = pd.DataFrame(methods, index=frame.index)
        rows.extend(evaluate_table(frame, target, methods, masks))
        pred = frame.loc[evaluate, ["series_id", "month", "target_month", f"y_{target}"]].join(table.loc[evaluate])
        pred["target"] = target
        prediction_tables.append(pred)
    results = pd.DataFrame(rows)
    results.to_csv(output / "metrics.csv", index=False)
    pd.concat(prediction_tables).to_csv(output / "predictions.csv", index=False)
    from visualization.experiment import plot_metrics
    plot_metrics(results, output / "test_mae.png")
    write_json(output / "briefing_input.json", {"metrics": json.loads(results.to_json(orient="records")),
                                               "availability": manifest["availability"]})
    manifest["elapsed_seconds"] = time.perf_counter() - start
    manifest["peak_memory_note"] = "Pico não instrumentado; execução local CPU, quatro threads CatBoost"
    write_json(output / "manifest.json", manifest)
    print(results[(results.split == "test") & (results.scope.isin(["available", "common"]))].to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", default=str(get_settings().raw_data_dir))
    parser.add_argument("--interim", default=str(DEFAULT_INTERIM))
    parser.add_argument("--start-month", metavar="AAAA-MM")
    parser.add_argument("--end-month", metavar="AAAA-MM")
    parser.add_argument("--output", required=True)
    parser.add_argument("--models", default="baselines,linear,tree,knn", help="Lista separada por vírgulas: baselines,linear,tree,knn,catboost,chronos")
    parser.add_argument("--knn-max-train", type=int, default=5000)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--chronos-sample-modulus", type=int, default=1024,
                        help="1 para todos os perfis; padrão 1024 limita o piloto CPU")
    parser.add_argument("--revision", default="29ec3766d36d6f73f0696f85560a422f50e8498c", help="Commit do checkpoint HF")
    args = parser.parse_args()
    for month in (args.start_month, args.end_month):
        if month is not None and file_month(f"scrdata_{month.replace('-', '')}.csv") != month:
            parser.error("As competências devem usar o formato AAAA-MM")
    if args.start_month and args.end_month and args.start_month > args.end_month:
        parser.error("--start-month deve ser anterior ou igual a --end-month")
    run(args)


if __name__ == "__main__":
    main()
