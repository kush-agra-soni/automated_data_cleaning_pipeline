# core/scaler.py

from sklearn.preprocessing import StandardScaler
from config.schema_config import SCALING_STRATEGY


def get_numerical_scaler():
    if SCALING_STRATEGY == "standard":
        return StandardScaler()
    else:
        raise NotImplementedError(f"Scaling strategy '{SCALING_STRATEGY}' is not supported yet.")
