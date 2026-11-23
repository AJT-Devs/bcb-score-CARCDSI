import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from config.constants import PROFILE_COLUMNS, BALANCE_COLUMNS, TARGET_DEFAULTS
from features.temporal import build_features
from models.temporal_validation import split_masks
from models.classical_regression import train_target, load_predict

class ClassicalTests(unittest.TestCase):
    def test_models_missing_unknown_reload_and_no_future_training(self):
        rows = []
        for sid in range(4):
            for month in range(1, 13):
                row = dict(series_id=sid, month=f'2025-{month:02}')
                row.update({c: f'category{sid}' for c in PROFILE_COLUMNS})
                row.update({c: 100. + sid for c in BALANCE_COLUMNS})
                row.update({t: .01 * month + .01 * sid for t in TARGET_DEFAULTS})
                rows.append(row)
        frame = build_features(pd.DataFrame(rows))
        frame.loc[frame.month.eq('2025-11'), 'uf'] = 'unseen'
        frame.loc[frame.month.eq('2025-11'), 'carteira_ativa'] = np.nan
        masks = split_masks(frame)
        with tempfile.TemporaryDirectory() as folder:
            for method in ('linear', 'tree', 'knn'):
                pred, info = train_target(frame, masks, TARGET_DEFAULTS[0], Path(folder), method, knn_max_train=7)
                loaded = load_predict(frame, Path(folder) / f'{method}_{TARGET_DEFAULTS[0]}.joblib')
                np.testing.assert_allclose(pred, loaded)
                self.assertTrue(np.isfinite(pred).all())
                self.assertEqual(info['training_rows'], 7 if method == 'knn' else 32)
                changed = frame.copy()
                changed.loc[~masks['train'], 'y_' + TARGET_DEFAULTS[0]] = 999
                _, after = train_target(changed, masks, TARGET_DEFAULTS[0], Path(folder), method, knn_max_train=7)
                np.testing.assert_allclose(pred, load_predict(frame, Path(folder) / f'{method}_{TARGET_DEFAULTS[0]}.joblib'))
                self.assertEqual(info['training_rows'], after['training_rows'])
