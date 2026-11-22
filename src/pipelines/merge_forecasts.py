"""Consolida execuções reais por chave exata, preservando as execuções de origem."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import time
import pandas as pd
from pipelines.evaluation_pipeline import evaluate_saved


def merge_runs(base, extra, output, interim, model="chronos"):
    tick = time.perf_counter()
    output.mkdir(parents=True, exist_ok=False)
    keys = ["series_id", "month", "target_month", "target"]
    primary = pd.read_csv(base / "predictions.csv")
    incoming = pd.read_csv(extra / "predictions.csv")
    extra_manifest = json.loads((extra / "manifest.json").read_text(encoding="utf-8"))
    expected_hash = hashlib.sha256((interim / "profiles.csv").read_bytes()).hexdigest()
    if extra_manifest.get("profile_key_sha256") != expected_hash:
        raise ValueError("Dicionário de perfis do experimento extra não corresponde ao painel")
    if primary.duplicated(keys).any() or incoming.duplicated(keys).any():
        raise ValueError("Previsões duplicadas na consolidação")
    if model in primary:
        raise ValueError("Modelo já existe no destino; não sobrescrever previsões")
    merged = primary.merge(incoming[[*keys, model]], on=keys, how="left", validate="one_to_one")
    merged.to_csv(output / "predictions.csv", index=False)
    for name in ("data_audit.json", "categories.json", "panel_audit.json", "temporal_audit.json"):
        if (base / name).exists():
            shutil.copyfile(base / name, output / name)
    if (base / "models").exists():
        shutil.copytree(base / "models", output / "models")
    manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
    manifest["upstream_runs"] = {"base": str(base), "extra": str(extra)}
    manifest["original_remote_attempt"] = manifest["models"].get(model)
    manifest["models"][model] = {"status": "executed", "source": str(extra), **extra_manifest}
    manifest["versions"][model] = importlib.metadata.version("chronos-forecasting")
    manifest["chronos_sample"] = "SHA256 da chave JSON UTF-8, módulo 1024 = 0; contexto três meses"
    manifest["final_source_hashes"] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path("src").rglob("*.py"))}
    manifest["source_hash_note"] = "Hashes na consolidação, não no início do treino. Refatorações de auditoria/avaliação após início; fórmulas, atributos, cortes e configuração dos modelos preservados."
    import subprocess
    import sys
    manifest["environment"] = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).splitlines()
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    result = evaluate_saved(output, interim)
    manifest["consolidation_seconds"] = time.perf_counter() - tick
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(result[(result.split == "test") & result.scope.isin(["available", "common"])].to_string(index=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("base", type=Path)
    p.add_argument("extra", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--interim", type=Path, default=Path("data/interim/2025"))
    a = p.parse_args()
    merge_runs(a.base, a.extra, a.output, a.interim)
