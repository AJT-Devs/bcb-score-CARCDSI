"""Fixtures exclusivamente sintéticas; não são resultados SCR."""
import unittest
import numpy as np
import pandas as pd
from config.constants import TARGET_DEFAULTS
from data.preprocessing.transformer import add_credit_ratios
from features.temporal import build_features
from models.baselines import predict_baselines
from models.evaluation import metrics
from models.temporal_validation import split_masks, split_origins
from models.chronos_forecast import ChronosForecaster


def panel():
    return pd.DataFrame({"series_id": [0, 0, 0, 1, 1],
        "month": ["2025-01", "2025-02", "2025-04", "2025-01", "2025-02"],
        **{t: [.1, .2, .9, .5, .6] for t in TARGET_DEFAULTS}})


class TemporalTests(unittest.TestCase):
    def test_exact_calendar_and_series(self):
        f = build_features(panel())
        self.assertEqual(f.loc[0, "y_" + TARGET_DEFAULTS[0]], .2)
        self.assertTrue(np.isnan(f.loc[1, "y_" + TARGET_DEFAULTS[0]]))
        self.assertTrue(np.isnan(f.loc[2, TARGET_DEFAULTS[0] + "_lag1"]))
        self.assertEqual(f.loc[3, "y_" + TARGET_DEFAULTS[0]], .6)

    def test_strict_past(self):
        p = panel()
        before = build_features(p)
        p.loc[p.month.eq("2025-04"), TARGET_DEFAULTS[0]] = 100
        after = build_features(p)
        cols = [c for c in before if not c.startswith("y_")]
        pd.testing.assert_frame_equal(before.loc[:1, cols], after.loc[:1, cols])

    def test_invalid_denominator_and_numerator(self):
        f = add_credit_ratios(pd.DataFrame({"carteira_ativa": [0, -1, np.inf, 10, 10],
            "carteira_inadimplencia": [1, 1, 1, 2, -1], "ativo_problematico": [1, 1, 1, 3, 11]}))
        self.assertTrue(f[TARGET_DEFAULTS[0]].iloc[:3].isna().all())
        self.assertEqual(f[TARGET_DEFAULTS[0]].iloc[3], .2)
        self.assertTrue(f[list(TARGET_DEFAULTS)].iloc[4].isna().all())

    def test_split_no_leak(self):
        f = pd.DataFrame({"month": [f"2025-{m:02}" for m in range(1, 13)]})
        m = split_masks(f)
        self.assertEqual(f.loc[m["train"], "month"].max(), "2025-08")
        self.assertEqual(f.loc[m["validation"], "month"].min(), "2025-09")
        self.assertFalse((m["train"] & m["test"]).any())

    def test_split_across_years_with_gap_and_saved_cut(self):
        months = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-03", "2025-04", "2025-05"]
        origins = split_origins(months)
        self.assertEqual(origins, {"train": ["2024-10", "2024-11"],
                                  "validation": ["2024-12", "2025-03"], "test": ["2025-04"]})
        sample = pd.DataFrame({"month": ["2025-03", "2025-04"]})
        masks = split_masks(sample, origins)
        self.assertEqual(masks["validation"].tolist(), [True, False])
        self.assertEqual(masks["test"].tolist(), [False, True])

    def test_metrics_and_coverage(self):
        r = metrics([0, 1, 1], [.1, .8, np.nan])
        self.assertEqual(r["n"], 2)
        self.assertAlmostEqual(r["mae"], .15)
        self.assertAlmostEqual(r["rmse"], np.sqrt(.025))
        self.assertAlmostEqual(r["r2"], .9)
        self.assertIsNone(metrics([1, 1], [1, 2])["r2"])
        self.assertIsNone(metrics([], [])["mae"])

    def test_baselines_abstain_on_gap(self):
        f = build_features(panel())
        p = predict_baselines(f, TARGET_DEFAULTS[0])
        self.assertEqual(p["naive"].iloc[1], .2)
        self.assertTrue(p["mean3"].isna().all())
        self.assertTrue(p["drift3"].isna().all())

    def test_duplicates_fail(self):
        p = panel()
        with self.assertRaises(ValueError):
            build_features(pd.concat([p, p.iloc[:1]]))

    def test_chronos_no_network_when_no_context(self):
        class Stub:
            def predict(self, *args, **kwargs):
                raise AssertionError("Não deveria prever contexto incompleto")
        f = build_features(panel())
        model = ChronosForecaster(pipeline=Stub())
        result = model.predict_target(f, TARGET_DEFAULTS[0], pd.Series(True, index=f.index))
        self.assertTrue(np.isnan(result).all())


if __name__ == "__main__":
    unittest.main()
