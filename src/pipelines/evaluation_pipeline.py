"""Recalcula métricas a partir de previsões salvas, sem retreinar modelos."""
import argparse
import json
from pathlib import Path
import pandas as pd
from config.constants import TARGET_DEFAULTS
from models.evaluation import evaluate_table
from models.temporal_validation import split_masks
from visualization.experiment import plot_metrics


def evaluate_saved(run, interim):
    predictions = pd.read_csv(run / "predictions.csv")
    profiles = pd.read_csv(interim / "profiles.csv", usecols=["series_id", "uf", "cliente", "segmento"])
    rows = []
    for target in TARGET_DEFAULTS:
        frame = predictions.loc[predictions.target.eq(target)].merge(profiles, on="series_id", validate="many_to_one")
        models = {c: frame[c] for c in ("naive", "mean3", "drift3", "catboost", "chronos") if c in frame}
        rows.extend(evaluate_table(frame, target, models, split_masks(frame)))
    table = pd.DataFrame(rows)
    table.to_csv(run / "metrics.csv", index=False)
    plot_metrics(table, run / "test_mae.png")
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    (run / "briefing_input.json").write_text(json.dumps({"metrics": json.loads(table.to_json(orient="records")),
        "availability": manifest["availability"]}, ensure_ascii=False, indent=2), encoding="utf-8")
    return table


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run", type=Path)
    p.add_argument("--interim", type=Path, default=Path("data/interim/2025"))
    a = p.parse_args()
    evaluate_saved(a.run, a.interim)
