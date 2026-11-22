"""Treinamento mínimo sintético para contrato de categorias/NaN e recarga."""
import tempfile
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from config.constants import PROFILE_COLUMNS, TARGET_DEFAULTS, BALANCE_COLUMNS
from features.temporal import build_features
from models.catboost_regression import train_target, load_predict
from models.temporal_validation import split_masks
from models.chronos_forecast import ChronosForecaster


class ModelTests(unittest.TestCase):
    def test_catboost_roundtrip_with_missing_numeric_and_new_category(self):
        rows = []
        for sid in (0, 1):
            for month in range(1, 13):
                row = dict(series_id=sid, month=f"2025-{month:02}")
                row.update({c: f"perfil sintético {sid}" for c in PROFILE_COLUMNS})
                row.update({c: 100. for c in BALANCE_COLUMNS})
                row.update({t: .01 * month + .1 * sid for t in TARGET_DEFAULTS})
                rows.append(row)
        frame = build_features(pd.DataFrame(rows))
        frame.loc[frame.month.eq("2025-11"), "uf"] = "nova sintética"
        with tempfile.TemporaryDirectory() as folder:
            predictions, _ = train_target(frame, split_masks(frame), TARGET_DEFAULTS[0], Path(folder))
            loaded = load_predict(frame, Path(folder) / f"{TARGET_DEFAULTS[0]}.cbm")
            np.testing.assert_allclose(predictions, loaded)
            self.assertTrue(np.isfinite(predictions).all())

    def test_chronos_context_and_median_contract(self):
        class Stub:
            quantiles = [.1, .5, .9]
            def predict(self, inputs, **kwargs):
                np.testing.assert_allclose(inputs[0], [.1, .2, .3])
                self.options = kwargs
                return [np.array([[[0.1], [0.25], [0.9]]])]
        t = TARGET_DEFAULTS[0]
        frame = pd.DataFrame({t: [.3], t + "_lag1": [.2], t + "_lag2": [.1]})
        stub = Stub()
        pred = ChronosForecaster(pipeline=stub).predict_target(frame, t, pd.Series([True]))
        self.assertEqual(pred[0], .25)
        self.assertEqual(stub.options["prediction_length"], 1)
        self.assertFalse(stub.options["cross_learning"])
