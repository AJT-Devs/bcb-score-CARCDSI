"""Chronos-2 local zero-shot, duas séries univariadas, sem covariáveis futuras."""
import numpy as np
import hashlib
from config.constants import TARGET_DEFAULTS


class ChronosForecaster:
    def __init__(self, checkpoint="amazon/chronos-2", revision=None, device="cpu", pipeline=None):
        if pipeline is None:
            from chronos import Chronos2Pipeline
            pipeline = Chronos2Pipeline.from_pretrained(checkpoint, revision=revision, device_map=device)
        self.pipeline = pipeline

    def predict_target(self, frame, target, mask):
        # Contexto comum de três meses completos; nenhuma compressão de lacunas.
        cols = [f"{target}_lag2", f"{target}_lag1", target]
        eligible = mask & frame[cols].notna().all(axis=1)
        output = np.full(len(frame), np.nan)
        indices = np.flatnonzero(eligible.to_numpy())
        for start in range(0, len(indices), 128):
            batch = indices[start:start + 128]
            inputs = [v.astype(np.float32) for v in frame.iloc[batch][cols].to_numpy()]
            forecasts = self.pipeline.predict(inputs, prediction_length=1, batch_size=128,
                                              context_length=3, cross_learning=False)
            q = list(self.pipeline.quantiles).index(0.5)
            output[batch] = [float(v[0, q, 0]) for v in forecasts]
        return output


def pilot_mask(frame, modulus=1024):
    """Amostra por SHA256 da chave, independente dos saldos e rótulos."""
    from config.constants import PROFILE_COLUMNS
    from functools import lru_cache
    import json
    if modulus < 1:
        raise ValueError("Módulo deve ser positivo")
    @lru_cache(maxsize=None)
    def selected(key):
        encoded = json.dumps(key, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return int(hashlib.sha256(encoded).hexdigest(), 16) % modulus == 0
    return frame[list(PROFILE_COLUMNS)].apply(lambda row: selected(tuple(row)), axis=1)
