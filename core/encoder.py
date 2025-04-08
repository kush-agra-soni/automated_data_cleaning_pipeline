# core/encoder.py

from sklearn.preprocessing import OneHotEncoder
from config.schema_config import ENCODING_STRATEGY


def get_categorical_encoder():
    if ENCODING_STRATEGY == "onehot":
        return OneHotEncoder(
            handle_unknown='ignore',
            sparse_output=False  # Dense output for easier integration with DataFrames
        )
    else:
        raise NotImplementedError(f"Encoding strategy '{ENCODING_STRATEGY}' is not supported yet.")
