import pandas as pd
from typing import List, Tuple
import warnings

# Threshold for dropping rows with excessive missing data
ROW_DROP_NAN_THRESHOLD = 0.5

# Column type placeholders
NUMERICAL_COLUMNS: List[str] = []
CATEGORICAL_COLUMNS: List[str] = []
IDENTIFIER_COLUMNS: List[str] = []
DATE_COLUMNS: List[str] = []


def infer_schema(df: pd.DataFrame, sample_size: int = 10) -> Tuple[List[str], List[str], List[str], List[str]]:
    numerical, categorical, identifier, date_cols = [], [], [], []

    sample = df.head(sample_size)
    for col in sample.columns:
        clean_col = col.strip().lower()

        # Treat ID-like columns
        if "id" in clean_col:
            identifier.append(col)
            continue

        col_data = sample[col].dropna()

        # Skip if no valid data
        if col_data.empty:
            continue

                # If numeric, skip date parsing
        try:
            numeric_vals = col_data.astype(float)
            if all(x.is_integer() for x in numeric_vals):
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].astype("Int64")
                numerical.append(col)
                continue
            else:
                numerical.append(col)
                continue
        except:
            pass  # Not numeric, continue to date check

              # Attempt date detection with warning suppressed
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            parsed_dates = pd.to_datetime(col_data, errors="coerce", dayfirst=True)

        if parsed_dates.notna().sum() >= len(col_data) * 0.6:
            date_cols.append(col)
            continue



        # Boolean detection (common patterns)
        bool_like = col_data.astype(str).str.lower().isin(["yes", "no", "true", "false", "0", "1"])
        if bool_like.sum() >= len(col_data) * 0.6:
            categorical.append(col)
            continue


        # Distinguish between int and float
        try:
            numeric_vals = col_data.astype(float)
            if all(x.is_integer() for x in numeric_vals):
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].astype("Int64")
                numerical.append(col)
            else:
                numerical.append(col)
        except:
            categorical.append(col)

    return numerical, categorical, identifier, date_cols


def load_and_infer_schema(file_path: str):
    global NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS, IDENTIFIER_COLUMNS, DATE_COLUMNS
    df = pd.read_csv(file_path)
    NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS, IDENTIFIER_COLUMNS, DATE_COLUMNS = infer_schema(df)
    return df