# core/imputer.py

from sklearn.impute import SimpleImputer
from config.schema_config import IMPUTATION_STRATEGY


def get_numerical_imputer():
    strategy = IMPUTATION_STRATEGY.get("numerical", "mean")
    return SimpleImputer(strategy=strategy)


def get_categorical_imputer():
    strategy = IMPUTATION_STRATEGY.get("categorical", "most_frequent")
    return SimpleImputer(strategy=strategy)
