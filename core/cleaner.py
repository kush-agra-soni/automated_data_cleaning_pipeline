import pandas as pd
from config.schema_config import (
    infer_schema  # this should be defined in your schema_config.py
)

def detect_and_print_column_types(df: pd.DataFrame):
    numerical, categorical, identifier, date_cols = infer_schema(df)

    column_types = {}
    for col in df.columns:
        dtype = df[col].dtype
        if col in identifier:
            column_types[col] = f"identifier({dtype})"
        elif col in numerical:
            column_types[col] = f"numerical({dtype})"
        elif col in categorical:
            column_types[col] = f"categorical({dtype})"
        elif col in date_cols:
            column_types[col] = f"date column(datetime)"
        else:
            column_types[col] = f"unknown({dtype})"

    print("\n>-- Inferred Column Types --<")
    for col, typ in column_types.items():
        print(f"{col} = {typ}")
