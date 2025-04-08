# How to run  ==  main_data_inject.py
# bash == python main_data_inject.py path/to/your_data.csv

import sys
import pandas as pd
from core.loader import load_data
from core.cleaner import clean_dataframe
from utils.file_utils import save_cleaned_data
from utils.logger import get_logger

logger = get_logger("main_data_inject")

def main(file_path: str):
    try:
        logger.info(f"Loading data from: {file_path}")
        df = load_data(file_path)

        logger.info("Starting data cleaning pipeline...")
        cleaned_df = clean_dataframe(df)

        output_path = save_cleaned_data(cleaned_df)
        logger.info(f"Cleaned data saved to: {output_path}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: Bash Command -->  python main_data_inject.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
