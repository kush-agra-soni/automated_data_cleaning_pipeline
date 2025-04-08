# core/transformer.py

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from config.schema_config import NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS

from core.imputer import get_numerical_imputer, get_categorical_imputer
from core.scaler import get_numerical_scaler
from core.encoder import get_categorical_encoder


def build_preprocessor():
    num_pipeline = Pipeline(steps=[
        ("imputer", get_numerical_imputer()),
        ("scaler", get_numerical_scaler())
    ])

    cat_pipeline = Pipeline(steps=[
        ("imputer", get_categorical_imputer()),
        ("encoder", get_categorical_encoder())
    ])

    transformer = ColumnTransformer(transformers=[
        ("num_pipeline", num_pipeline, NUMERICAL_COLUMNS),
        ("cat_pipeline", cat_pipeline, CATEGORICAL_COLUMNS)
    ],
        remainder='drop',
        n_jobs=-1
    )

    return transformer
