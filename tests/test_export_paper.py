"""Exportação das evidências numéricas sem dados de produção."""
import json
from pathlib import Path
import tempfile
import unittest
import pandas as pd
from visualization.export_paper import export


class ExportPaperTests(unittest.TestCase):
    def test_model_names_and_times_come_from_run(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run, dest = root / 'run', root / 'paper'
            run.mkdir()
            (run / 'models').mkdir()
            pd.DataFrame([dict(split='test', scope=scope, target='proporcao_inadimplencia',
                model='knn', n=3, n_eligible=4, coverage=.75, mae_pp=1.0, rmse_pp=2.0,
                r2=.3, out_of_range=1) for scope in ('available', 'common')]).to_csv(run / 'metrics.csv', index=False)
            (run / 'manifest.json').write_text(json.dumps({'models': {'knn': {'status': 'executed', 'seconds': 12.34}}}), encoding='utf-8')
            (run / 'data_audit.json').write_text(json.dumps([{'rows': 4, 'bytes': 123}]), encoding='utf-8')
            export(run, dest)
            self.assertIn('k-NN', (dest / 'results.tex').read_text(encoding='utf-8'))
            self.assertIn('12,34', (dest / 'runtime.tex').read_text(encoding='utf-8'))
