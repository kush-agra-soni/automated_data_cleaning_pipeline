import pandas as pd
from config.schema_config import (
    ROW_DROP_NAN_THRESHOLD,
    NUMERICAL_COLUMNS,
    CATEGORICAL_COLUMNS,
    IDENTIFIER_COLUMNS,
    DATE_COLUMNS
)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def drop_high_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    threshold = int((1 - ROW_DROP_NAN_THRESHOLD) * df.shape[1])
    return df.dropna(thresh=threshold)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].ffill().bfill()
    return df


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if col in NUMERICAL_COLUMNS:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ["float64", "int64"]:
                    df[col] = df[col].fillna(df[col].median())
        elif col in CATEGORICAL_COLUMNS:
            if df[col].isnull().sum() > 0:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])
                else:
                    df[col] = df[col].fillna("Unknown")

    # Recast float64 back to int where possible
    for col in NUMERICAL_COLUMNS:
        if col in df.columns and pd.api.types.is_float_dtype(df[col]):
            if df[col].dropna().apply(float.is_integer).all():
                df[col] = df[col].astype("Int64")

    return df


def normalize_booleans(df: pd.DataFrame) -> pd.DataFrame:
    true_set = {"yes", "true", "1"}
    false_set = {"no", "false", "0"}

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            unique_vals = df[col].dropna().astype(str).str.lower().unique()
            if set(unique_vals).issubset(true_set.union(false_set)):
                df[col] = df[col].astype(str).str.lower().map(lambda x: True if x in true_set else False)
    return df


def trim_string_values(df: pd.DataFrame) -> pd.DataFrame:
    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.strip()
    return df.drop_duplicates().reset_index(drop=True)


def run_cleaning_steps(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_high_nan_rows(df)
    df = parse_dates(df)
    df = impute_missing_values(df)
    df = normalize_booleans(df)
    df = trim_string_values(df)
    df = remove_duplicates(df)
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return run_cleaning_steps(df)


# --------------------------------------------------------------
# 📏 TEMPORARY TEST BLOCK — FOR DEBUGGING CLEANING ONLY
# --------------------------------------------------------------
if __name__ == "__main__":
    import os
    input_path = "messy_data.csv"
    output_path = os.path.join("output_data", "cleaned.csv")

    print(f">-- Loading test file: {input_path} --<")
    df = pd.read_csv(input_path)
    cleaned = clean_dataframe(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    print(f">-- Cleaned data saved to: {output_path} --<")
# --------------------------------------------------------------
# 📏 END OF TEMPORARY TEST BLOCK
# --------------------------------------------------------------