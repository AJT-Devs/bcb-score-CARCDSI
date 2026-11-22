"""Piloto Chronos isolado sobre o painel preparado; não retreina CatBoost."""
import argparse
import json
from pathlib import Path
import time
import hashlib
import pandas as pd
from config.constants import TARGET_DEFAULTS
from models.chronos_forecast import ChronosForecaster, pilot_mask
from models.baselines import predict_baselines
from models.evaluation import evaluate_table
from models.temporal_validation import split_masks


def run(interim, output, modulus=1024):
    import torch
    torch.set_num_threads(4)
    output.mkdir(parents=True, exist_ok=False)
    tick = time.perf_counter()
    profiles = pd.read_csv(interim / "profiles.csv")
    ids = profiles.loc[pilot_mask(profiles, modulus), "series_id"]
    parts = []
    for chunk in pd.read_csv(interim / "supervised.csv", chunksize=100000):
        parts.append(chunk.loc[chunk.series_id.isin(ids)])
    frame = pd.concat(parts, ignore_index=True)
    checkpoint = ".tools/chronos-2" if Path(".tools/chronos-2/model.safetensors").exists() else "amazon/chronos-2"
    model = ChronosForecaster(checkpoint=checkpoint, revision="29ec3766d36d6f73f0696f85560a422f50e8498c")
    masks = split_masks(frame)
    selected = masks["validation"] | masks["test"]
    rows, tables = [], []
    for target in TARGET_DEFAULTS:
        methods = predict_baselines(frame, target)
        methods["chronos"] = model.predict_target(frame, target, selected)
        rows.extend(evaluate_table(frame, target, methods, masks))
        table = frame.loc[selected, ["series_id", "month", "target_month", f"y_{target}"]].join(pd.DataFrame(methods).loc[selected])
        table["target"] = target
        tables.append(table)
    pd.concat(tables).to_csv(output / "predictions.csv", index=False)
    pd.DataFrame(rows).to_csv(output / "metrics.csv", index=False)
    (output / "manifest.json").write_text(json.dumps({"modulus": modulus, "selected_profile_keys": len(ids),
        "profile_key_sha256": hashlib.sha256((interim / "profiles.csv").read_bytes()).hexdigest(),
        "seconds": time.perf_counter() - tick, "fine_tuning": False,
        "revision": "29ec3766d36d6f73f0696f85560a422f50e8498c", "context": 3, "device": "cpu"}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--interim", type=Path, default=Path("data/interim/2025"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--modulus", type=int, default=1024)
    a = p.parse_args()
    run(a.interim, a.output, a.modulus)
