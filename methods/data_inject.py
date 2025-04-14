import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tabulate import tabulate
from tkinter import filedialog
from core.1_loader import load_file
from core.2_detector import detection


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
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    try:
        dataframe, final_column_types = detection(dataframe)
        print("Column Types:")
        table = [[column, dtype] for column, dtype in final_column_types.items()]
        print(tabulate(table, headers=["Column Name", "Detected Data Type"], tablefmt="grid"))
    except Exception as e:
        print(f"Error during detection: {e}")


def main():
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting.")
        exit(1)
    process_file(file_path)

if __name__ == "__main__":
    main()