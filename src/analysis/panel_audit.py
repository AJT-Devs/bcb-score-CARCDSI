"""Auditoria complementar de meses, contexto e mudanças de categorias."""
import argparse
import json
from pathlib import Path
import pandas as pd
from config.constants import PROFILE_COLUMNS, TARGET_DEFAULTS


def audit_prepared(path, output):
    columns = ["month", "series_id", *PROFILE_COLUMNS,
               *[f"y_{t}" for t in TARGET_DEFAULTS], *[f"{t}_mean3" for t in TARGET_DEFAULTS]]
    months, profiles, previous, counts = {}, set(), {}, {}
    for chunk in pd.read_csv(path, usecols=columns, chunksize=100000):
        for month, part in chunk.groupby("month"):
            info = months.setdefault(month, {"rows": 0, "missing_next_target": {t: 0 for t in TARGET_DEFAULTS},
                "missing_three_month_context": {t: 0 for t in TARGET_DEFAULTS}, "categories": {c: set() for c in PROFILE_COLUMNS}})
            info["rows"] += len(part)
            profiles.update(part.series_id)
            for sid, n in part.series_id.value_counts().items():
                counts[int(sid)] = counts.get(int(sid), 0) + int(n)
            for t in TARGET_DEFAULTS:
                info["missing_next_target"][t] += int(part[f"y_{t}"].isna().sum())
                info["missing_three_month_context"][t] += int(part[f"{t}_mean3"].isna().sum())
            for col in PROFILE_COLUMNS:
                info["categories"][col].update(part[col].unique())
    for month in sorted(months):
        info = months[month]
        sets = info.pop("categories")
        info["category_changes"] = {c: {"added": sorted(sets[c] - previous.get(c, set())),
                                        "removed": sorted(previous.get(c, set()) - sets[c])}
                                    for c in PROFILE_COLUMNS}
        previous = sets
    calendar = pd.period_range(min(months), max(months), freq="M").astype(str) if months else []
    result = {"months": months, "missing_months": sorted(set(calendar) - set(months)),
              "profiles": len(profiles), "profile_observation_counts": pd.Series(counts).value_counts().sort_index().to_dict()}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prepared", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    audit_prepared(a.prepared, a.output)
