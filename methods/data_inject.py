import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tabulate import tabulate # type: ignore
from tkinter import filedialog
from core._1_loader import load_file
from core._2_detector import datadetector
from core._3_cleaner import cleaning
from core._4_standardizer import standardizer


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
        print("Before detection:")
        print(dataframe.info())
        print(dataframe.to_string())

        detector = datadetector()
        dataframe, column_types = detector.detection(dataframe)

        print("After detection:")
        print(dataframe.info())
        print(dataframe.to_string())

        dataframe = run_cleaning(dataframe)
        # dataframe = run_standardizer(dataframe)
    except Exception as e:
        print(f"Error: {e}")


def run_cleaning(dataframe):
    """Apply all cleaning methods from the Cleaning class to the DataFrame."""
    cleaner = cleaning()
    dataframe = cleaner.run_cleaning(dataframe)
    print(dataframe.to_string())
    return dataframe


def run_standardizer(df):
    standardizer_instance = standardizer()
    df = standardizer_instance.format_all(df)
    print(df.to_string())  # Preview the standardized DataFrame
    return df


def main():
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting.")
        exit(1)
    process_file(file_path)

if __name__ == "__main__":
    main()