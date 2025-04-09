import tkinter as tk
from tkinter import filedialog
from core.loader import load_file
from core.cleaner import clean_dataframe

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

    df = load_file(file_path)
    cleaned_df = clean_dataframe(df)

    print("\n>--Cleaned Data Preview--<\n")
    print(cleaned_df.head(55))