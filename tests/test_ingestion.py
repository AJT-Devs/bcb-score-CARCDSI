"""Integração com arquivos pequenos e sintéticos, sem rede."""
import tempfile
from pathlib import Path
import unittest
import pandas as pd
from config.constants import PROFILE_COLUMNS, BALANCE_COLUMNS, TARGET_DEFAULTS
from data.read.panel import load_panel
from features.temporal import build_features
from models.catboost_regression import model_inputs


class IngestionTests(unittest.TestCase):
    def test_csv_to_targets_and_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for month in (1, 2, 4):
                row = {c: "categoria sintética" for c in PROFILE_COLUMNS}
                row.update(data_base=f"2025-{month:02}-28", carteira_ativa="10,0",
                           carteira_inadimplencia="2,0", ativo_problematico="3,0")
                pd.DataFrame([row]).to_csv(root / f"scrdata_2025{month:02}.csv", sep=";", index=False)
            panel, audit, _ = load_panel(root, root / "interim")
            frame = build_features(panel)
            self.assertEqual(len(audit), 3)
            self.assertEqual(frame.loc[0, f"y_{TARGET_DEFAULTS[0]}"], .2)
            self.assertTrue(pd.isna(frame.loc[1, f"y_{TARGET_DEFAULTS[0]}"]))
            self.assertEqual(model_inputs(frame).carteira_ativa.iloc[0], 10)

    def test_duplicate_rows_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            row = {c: "sintético" for c in PROFILE_COLUMNS}
            row.update({c: "1,0" for c in BALANCE_COLUMNS})
            row["data_base"] = "2025-01-31"
            pd.DataFrame([row, row]).to_csv(root / "scrdata_202501.csv", sep=";", index=False)
            with self.assertRaises(ValueError):
                load_panel(root, root / "out")
