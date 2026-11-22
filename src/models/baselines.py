"""Referências com histórico contíguo, sem imputação futura."""


def predict_baselines(frame, target):
    current, lag1, lag2 = frame[target], frame[f"{target}_lag1"], frame[f"{target}_lag2"]
    return {"naive": current, "mean3": frame[f"{target}_mean3"],
            "drift3": (current + (current - lag2) / 2).where(current.notna() & lag1.notna() & lag2.notna())}
