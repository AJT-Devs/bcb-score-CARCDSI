"""Ingestão estrita em chunks; nenhuma agregação implícita de perfis."""
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np
from config.constants import PROFILE_COLUMNS, BALANCE_COLUMNS, TARGET_DEFAULTS, REQUIRED_COLUMNS
from data.read.monthly_files import monthly_files
from data.preprocessing.transformer import add_credit_ratios
from data.validation.data_validator import validate_required_columns
from data.validation.panel_validator import validate_month, valid_profile_mask, validate_unique_keys


def load_panel(raw: Path, output: Path, start=None, end=None):
    output.mkdir(parents=True, exist_ok=True)
    frames, audit, categories = [], [], {}
    for month, path in monthly_files(raw, start, end):
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        chunks, invalid = [], 0
        for chunk in pd.read_csv(path, sep=";", encoding="utf-8-sig", decimal=",", dtype=str,
                                 usecols=lambda col: col in REQUIRED_COLUMNS, keep_default_na=False, chunksize=50000):
            validate_required_columns(chunk.columns)
            for col in PROFILE_COLUMNS:
                categories.setdefault(col, set()).update(chunk[col].unique())
            frame = chunk
            frame["month"] = pd.to_datetime(frame.pop("data_base"), errors="raise").dt.to_period("M").astype(str)
            validate_month(frame, month, path.name)
            for col in BALANCE_COLUMNS:
                frame[col] = pd.to_numeric(frame[col].str.replace(",", ".", regex=False), errors="coerce")
            valid = valid_profile_mask(frame)
            invalid += int((~valid).sum())
            chunks.append(frame.loc[valid])
        monthly = pd.concat(chunks, ignore_index=True)
        validate_unique_keys(monthly, path.name)
        monthly = add_credit_ratios(monthly)
        report = {"file": path.name, "bytes": path.stat().st_size, "sha256": digest,
                  "mtime_utc": pd.Timestamp(path.stat().st_mtime, unit="s", tz="UTC").isoformat(),
                  "rows": len(monthly), "missing_key_excluded": invalid,
                  "invalid_denominator": int((~np.isfinite(monthly.carteira_ativa) | (monthly.carteira_ativa <= 0)).sum()),
                  "invalid_targets": {t: int(monthly[t].isna().sum()) for t in TARGET_DEFAULTS}}
        monthly.to_csv(output / f"{path.stem}.csv", index=False)
        audit.append(report)
        frames.append(monthly)
    if not frames:
        raise FileNotFoundError(f"Nenhum CSV mensal em {raw} no intervalo selecionado")
    panel = pd.concat(frames, ignore_index=True)
    # Códigos estáveis durante a execução; chave completa é salva em separado.
    keys = panel[list(PROFILE_COLUMNS)].drop_duplicates().reset_index(drop=True)
    keys["series_id"] = keys.index
    panel = panel.merge(keys, on=list(PROFILE_COLUMNS), validate="many_to_one")
    keys.to_csv(output / "profiles.csv", index=False)
    return panel, audit, {c: sorted(v) for c, v in categories.items()}
