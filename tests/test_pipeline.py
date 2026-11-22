"""Integração completa offline com 24 linhas inteiramente sintéticas."""
from argparse import Namespace
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
import pandas as pd
from config.constants import PROFILE_COLUMNS
from pipelines.experiment import run
from pipelines.evaluation_pipeline import evaluate_saved


class PipelineTests(unittest.TestCase):
    def test_ingest_train_save_predict_evaluate(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            raw = root / "raw"
            raw.mkdir()
            for month in range(1, 13):
                rows = []
                for sid in (0, 1):
                    row = {c: f"categoria sintética {sid}" for c in PROFILE_COLUMNS}
                    row.update(data_base=f"2025-{month:02}-28", carteira_ativa="100,0",
                               carteira_inadimplencia=str(month + sid), ativo_problematico=str(month + sid + 1))
                    rows.append(row)
                pd.DataFrame(rows).to_csv(raw / f"scrdata_2025{month:02}.csv", sep=";", index=False)
            args = Namespace(raw=str(raw), interim=str(root / "interim"), output=str(root / "run"),
                             models="catboost", revision="unused-offline", device="cpu", chronos_sample_modulus=1024)
            with redirect_stdout(io.StringIO()):
                run(args)
            output = root / "run"
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["models"]["catboost"]["status"], "executed")
            before = pd.read_csv(output / "metrics.csv")
            after = evaluate_saved(output, root / "interim")
            pd.testing.assert_frame_equal(before, after, check_dtype=False, atol=1e-12)
            test = after[(after.split == "test") & (after.scope == "common")]
            self.assertTrue(test.n.eq(2).all())
            self.assertTrue((output / "models/proporcao_inadimplencia.cbm").exists())
