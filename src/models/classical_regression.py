"""Regressores clássicos com pré-processamento ajustado somente no treino."""
import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
from config.constants import PROFILE_COLUMNS
from models.catboost_regression import feature_columns


def model_inputs(frame):
    x = frame[feature_columns()].copy().replace([np.inf, -np.inf], np.nan)
    for col in PROFILE_COLUMNS:
        x[col] = x[col].fillna('__MISSING__').astype(str)
    return x


def train_target(frame, masks, target, output: Path, method, knn_max_train=5000, prediction_mask=None):
    if knn_max_train < 1:
        raise ValueError('knn_max_train deve ser positivo')
    y = frame[f'y_{target}']
    eligible = masks['train'] & y.notna() & np.isfinite(y)
    indices = frame.index[eligible]
    if not len(indices):
        raise ValueError('Treino sem rótulos válidos')
    total = len(indices)
    if method == 'knn' and total > knn_max_train:
        indices = frame.loc[indices].sample(n=knn_max_train, random_state=42).index
    numeric = [c for c in feature_columns() if c not in PROFILE_COLUMNS]
    pre = ColumnTransformer([
        ('numeric', Pipeline([('impute', SimpleImputer(strategy='median', keep_empty_features=True)),
                              ('scale', StandardScaler())]), numeric),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), list(PROFILE_COLUMNS)),
    ], sparse_threshold=1.0)
    choices = {'linear': LinearRegression(),
               'tree': DecisionTreeRegressor(max_depth=12, min_samples_leaf=5, random_state=42),
               'knn': KNeighborsRegressor(n_neighbors=min(5, len(indices)), algorithm='brute', n_jobs=1)}
    if method not in choices:
        raise ValueError(f'Modelo desconhecido: {method}')
    pipeline = Pipeline([('preprocess', pre), ('model', choices[method])])
    x = model_inputs(frame)
    pipeline.fit(x.loc[indices], y.loc[indices])
    output.mkdir(parents=True, exist_ok=True)
    path = output / f'{method}_{target}.joblib'
    joblib.dump(pipeline, path)
    info = {'method': method, 'target': target, 'features': feature_columns(),
            'training_rows': len(indices), 'eligible_training_rows': total,
            'sampling': 'amostra uniforme sem reposição, somente treino, random_state=42' if len(indices) < total else 'todas as linhas elegíveis de treino',
            'knn_max_train': knn_max_train if method == 'knn' else None,
            'parameters': pipeline.named_steps['model'].get_params(), 'refit': False}
    (output / f'{method}_{target}.json').write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding='utf-8')
    if prediction_mask is None:
        return predict_batches(pipeline, x), info
    predictions = np.full(len(frame), np.nan)
    mask = np.asarray(prediction_mask, dtype=bool)
    predictions[mask] = predict_batches(pipeline, x.loc[mask])
    return predictions, info


def predict_batches(pipeline, x, batch_size=1000):
    return np.concatenate([pipeline.predict(x.iloc[i:i + batch_size]) for i in range(0, len(x), batch_size)]) if len(x) else np.array([])


def load_predict(frame, model_path):
    return predict_batches(joblib.load(model_path), model_inputs(frame))
