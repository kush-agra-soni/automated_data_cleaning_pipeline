# core/cleaner.py

import pandas as pd
from config.schema_config import ROW_DROP_NAN_THRESHOLD, CATEGORICAL_COLUMNS


def drop_high_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    threshold = int((1 - ROW_DROP_NAN_THRESHOLD) * df.shape[1])
    return df.dropna(thresh=threshold)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def trim_string_values(df: pd.DataFrame) -> pd.DataFrame:
    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def run_cleaning_steps(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_high_nan_rows(df)
    df = trim_string_values(df)
    return df
