"""Exporta somente resultados calculados; sem valores predefinidos no artigo."""
import argparse
import json
from pathlib import Path
import shutil
import pandas as pd


def export(run, destination):
    destination.mkdir(parents=True, exist_ok=True)
    table = pd.read_csv(run / "metrics.csv")
    selected = table[(table.split == "test") & (table.scope == "common")]
    labels = {"naive": "Ingênuo", "mean3": "Média3", "drift3": "Drift3", "catboost": "CatBoost", "chronos": "Chronos-2", "linear": "Linear", "tree": "Árvore", "knn": "k-NN", "baselines": "Baselines"}
    lines = [r"\begin{table}[ht]", r"\centering", r"\caption{Teste em dezembro: interseção dos métodos executados, sem clipping.}",
             r"\label{tab:results}", r"\small", r"\begin{tabular}{llrrrr}", r"\hline", r"Alvo & Método & $n$ & MAE (pp) & RMSE (pp) & $R^2$ \\", r"\hline"]
    def decimal(value, places=3):
        return f"{value:.{places}f}".replace(".", ",")
    for _, row in selected.iterrows():
        target = "Inad." if row.target == "proporcao_inadimplencia" else "Problem."
        r2 = decimal(row.r2) if pd.notna(row.r2) else "--"
        lines.append(f"{target} & {labels.get(row.model, row.model)} & {int(row.n)} & {decimal(row.mae_pp)} & {decimal(row.rmse_pp)} & {r2} " + r"\\")
    lines += [r"\hline", r"\end{tabular}", r"\end{table}"]
    (destination / "results.tex").write_text("\n".join(lines), encoding="utf-8")
    available = table[(table.split == "test") & (table.scope == "available")]
    coverage = [r"\begin{table}[ht]", r"\centering", r"\caption{Cobertura no conjunto total de rótulos elegíveis do teste.}",
                r"\label{tab:coverage}", r"\small", r"\begin{tabular}{llrrr}", r"\hline",
                r"Alvo & Método & Previsões avaliadas & Cobertura (\%) & Fora de [0,1] \\", r"\hline"]
    for _, row in available.iterrows():
        target = "Inad." if row.target == "proporcao_inadimplencia" else "Problem."
        coverage.append(f"{target} & {labels.get(row.model, row.model)} & {int(row.n)} & {decimal(100*row.coverage)} & {int(row.out_of_range)} " + r"\\")
    coverage += [r"\hline", r"\end{tabular}", r"\end{table}"]
    (destination / "coverage.tex").write_text("\n".join(coverage), encoding="utf-8")
    discussion = []
    for target, group in selected.groupby("target"):
        if group.mae_pp.notna().any():
            best = group.loc[group.mae_pp.idxmin()]
            label = "inadimplência" if target == "proporcao_inadimplencia" else "ativos problemáticos"
            discussion.append(f"Para {label}, o menor MAE foi do método {labels.get(best.model, best.model)}: "
                              f"{decimal(best.mae_pp)} pp em {int(best.n)} perfis.")
    discussion.append("A ordenação por MAE em um único mês não demonstra superioridade geral; RMSE e cobertura devem ser considerados conjuntamente.")
    (destination / "discussion.tex").write_text(" ".join(discussion), encoding="utf-8")
    if (run / "test_mae.png").exists():
        shutil.copyfile(run / "test_mae.png", destination / "test_mae.png")
    # Evidência pequena versionável; previsões e modelos ficam em runs/ ignorado.
    table.to_csv(destination / "metrics.csv", index=False)
    for name in ("manifest.json", "data_audit.json"):
        shutil.copyfile(run / name, destination / name)
    for configuration in (run / "models").glob("*.json"):
        shutil.copyfile(configuration, destination / configuration.name)
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    durations = []
    for name, info in manifest.get("models", {}).items():
        if info.get("status") == "executed" and isinstance(info.get("seconds"), (int, float)):
            seconds = f"{info['seconds']:.2f}".replace(".", ",")
            durations.append(f"{labels.get(name, name)}: {seconds} s")
    if durations:
        (destination / "runtime.tex").write_text(
            "Os tempos medidos foram " + "; ".join(durations) + ". Os tempos dos modelos supervisionados incluem os dois alvos e suas previsões; o tempo do Chronos inclui leitura do painel preparado. Não são tempos de inferência isolada.",
            encoding="utf-8")
    audit = json.loads((run / "data_audit.json").read_text(encoding="utf-8"))
    def number(value):
        return f"{value:,}".replace(",", ".")
    summary = f"A base contém {number(sum(a['rows'] for a in audit))} observações perfil/mês em {len(audit)} meses. "
    if (run / "panel_audit.json").exists():
        shutil.copyfile(run / "panel_audit.json", destination / "panel_audit.json")
        panel = json.loads((run / "panel_audit.json").read_text(encoding="utf-8"))
        summary += f"Foram identificados {number(panel['profiles'])} perfis distintos; somente {number(panel['profile_observation_counts'].get('12', 0))} aparecem nos doze meses. "
        summary += "As ausências de perfil entre meses reduzem a amostra supervisionada e não representam saldo zero."
    (destination / "data-summary.tex").write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("run", type=Path)
    p.add_argument("--destination", type=Path, default=Path("paper/generated"))
    a = p.parse_args()
    export(a.run, a.destination)
