import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tabulate import tabulate # type: ignore
from tkinter import filedialog
from core.loader_1 import load_file
from core.detector_2 import detection
from core.cleaner_3 import Cleaning


def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select Data File",
        filetypes=[("CSV files", "*.csv"),
                   ("JSON files", "*.json"),
                   ("Excel files", "*.xlsx")
                   ])


def process_file(file_path):
    print(f"Processing file: {file_path}")

    try:
        dataframe = load_file(file_path)
        dataframe, final_column_types = detection(dataframe)
        print(tabulate([[col, dtype] for col, dtype in final_column_types.items()], 
                      headers=["Column Name", "Detected Data Type"], tablefmt="grid"))
        dataframe = apply_all_cleaning_methods(dataframe)
        print(dataframe.head(15))
    except Exception as e:
        print(f"Error: {e}")


def apply_all_cleaning_methods(dataframe):
    """Apply all cleaning methods from the Cleaning class to the DataFrame."""
    cleaner = Cleaning()
    dataframe = cleaner.remove_special_characters(dataframe)
    dataframe = cleaner.convert_to_lowercase(dataframe)
    dataframe = cleaner.remove_whitespace(dataframe)
    dataframe = cleaner.replace_space_with_underscore(dataframe)
    dataframe = cleaner.identifier_column_remover(dataframe)
    dataframe = cleaner.remove_empty_columns(dataframe)
    dataframe = cleaner.remove_empty_rows(dataframe)
    dataframe = cleaner.remove_duplicates(dataframe)
    dataframe = cleaner.extract_dates(dataframe)
    print(dataframe.head(15))
    return dataframe



def main():
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting.")
        exit(1)
    process_file(file_path)

if __name__ == "__main__":
    main()