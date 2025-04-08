# core/loader.py

import pandas as pd
import os

SUPPORTED_FORMATS = ['.csv', '.json', '.xlsx']

def load_file(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {ext}")

    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext == '.json':
        df = pd.read_json(file_path)
    elif ext == '.xlsx':
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type.")

    return df


# Optional placeholder for scheduled DB ingestion
def load_from_database(query: str, connection) -> pd.DataFrame:
    """
    Example usage:
    from sqlalchemy import create_engine
    engine = create_engine('your_connection_string')
    df = load_from_database('SELECT * FROM your_table', engine)
    """
    return pd.read_sql_query(query, connection)
