# utils/file_utils.py

import os
import pandas as pd
from datetime import datetime

OUTPUT_DIR = "data_cleaning_pipeline/output/cleaned_data"

def save_cleaned_data(df: pd.DataFrame, file_name: str = None) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not file_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"cleaned_data_{timestamp}.csv"

    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path, index=False)

    return output_path
