import tkinter as tk
from tkinter import filedialog
from core.loader import load_file
from core.cleaner import detect_and_print_column_types  # Import more functions if needed

def run_file_selector():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=">--Select Data File--<",
        filetypes=[
            ("CSV files", "*.csv"),
            ("JSON files", "*.json"),
            ("Excel files", "*.xlsx")
        ]
    )
    return file_path

if __name__ == "__main__":
    file_path = run_file_selector()

    if not file_path:
        print(">--No file selected. Exiting.--<")
        exit(1)

    df = load_file(file_path)  # Load using loader
    detect_and_print_column_types(df)  # Call your cleaner function

    # 👉 If you want to use more functions from cleaner.py
    # from core.cleaner import clean_column_names, drop_high_nan_rows, ... etc.
    # Then call them one by one like:
    # df = clean_column_names(df)
    # df = drop_high_nan_rows(df)
