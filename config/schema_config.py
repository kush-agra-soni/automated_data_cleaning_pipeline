import pandas as pd
from typing import List, Tuple

# Threshold for dropping rows with excessive missing data
ROW_DROP_NAN_THRESHOLD = 0.5

# Auto-schema placeholders (used in pipeline if dynamic inference is on)
NUMERICAL_COLUMNS: List[str] = []
CATEGORICAL_COLUMNS: List[str] = []
IDENTIFIER_COLUMNS: List[str] = []
DATE_COLUMNS: List[str] = []


def infer_schema(df: pd.DataFrame, sample_size: int = 10) -> Tuple[List[str], List[str], List[str], List[str]]:
    numerical = []
    categorical = []
    identifier = []
    date_cols = []

    sample = df.head(sample_size)
    for col in sample.columns:
        col_lower = col.strip().lower()

        if "id" in col_lower:
            identifier.append(col)
            continue

        # Attempt to parse date columns
        try:
            parsed = pd.to_datetime(sample[col], errors="coerce")
            if parsed.notna().sum() > 0:
                date_cols.append(col)
                continue
        except Exception:
            pass

        if pd.api.types.is_numeric_dtype(sample[col]):
            numerical.append(col)
        elif pd.api.types.is_string_dtype(sample[col]) or sample[col].dtype == "object":
            categorical.append(col)

    return numerical, categorical, identifier, date_cols


def load_and_infer_schema(file_path: str):
    global NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS, IDENTIFIER_COLUMNS, DATE_COLUMNS
    df = pd.read_csv(file_path)
    NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS, IDENTIFIER_COLUMNS, DATE_COLUMNS = infer_schema(df)
    return df
