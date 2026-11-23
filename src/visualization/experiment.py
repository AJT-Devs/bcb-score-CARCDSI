"""Figuras derivadas exclusivamente da tabela de avaliação."""
def plot_metrics(table, path):
    import os
    from pathlib import Path
    import tempfile
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "carcdsi-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data = table[(table.split == "test") & (table.scope == "common")]
    if data.empty or not data.mae_pp.notna().any():
        return
    pivot = data.pivot(index="model", columns="target", values="mae_pp")
    pivot = pivot.reindex([m for m in ("naive", "mean3", "drift3", "linear", "tree", "knn", "catboost", "chronos") if m in pivot.index])
    pivot = pivot.rename(index={"naive": "Ingênuo", "mean3": "Média3", "drift3": "Drift3", "linear": "Linear", "tree": "Árvore", "knn": "k-NN", "catboost": "CatBoost", "chronos": "Chronos-2"},
                         columns={"proporcao_inadimplencia": "Inadimplência", "proporcao_ativos_problematicos": "Ativos problemáticos"})
    pivot.columns.name = None
    ax = pivot.plot.bar(figsize=(9, 4), color=["0.25", "0.65"])
    ax.set_ylabel("MAE (pontos percentuais)")
    ax.set_xlabel("Método; interseção dos métodos executados")
    ax.tick_params(axis="x", labelrotation=0)
    ax.figure.tight_layout()
    ax.figure.savefig(path, dpi=200)
    plt.close(ax.figure)
