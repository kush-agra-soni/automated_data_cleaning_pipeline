import os
import pandas as pd # type: ignore

SUPPORTED_FORMATS = ['.csv', '.json', '.xlsx']

def load_file(file_path: str) -> pd.DataFrame:
    """Load data from a file into a pandas DataFrame."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {ext}")

    loaders = {
        '.csv': pd.read_csv,
        '.json': pd.read_json,
        '.xlsx': pd.read_excel
    }

    return loaders[ext](file_path)

def load_from_database(query: str, connection) -> pd.DataFrame:
    """Executes a SQL query and loads the result into a pandas 
    DataFrame using the provided connection."""
    return pd.read_sql_query(query, connection)