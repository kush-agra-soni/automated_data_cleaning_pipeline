import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fit bounds using IQR or Z-Score
def fit_outlier_bounds(df: pd.DataFrame, method: str = "iqr", z_thresh: float = 3.0, iqr_multiplier: float = 1.5) -> dict:
    bounds = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        col_data = df[col].dropna()

        if method == "zscore":
            mean = col_data.mean()
            std = col_data.std()
            lower = mean - z_thresh * std
            upper = mean + z_thresh * std

        elif method == "iqr":
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - iqr_multiplier * IQR
            upper = Q3 + iqr_multiplier * IQR

        else:
            raise ValueError("Method must be 'zscore' or 'iqr'")

        bounds[col] = (lower, upper)

    print(f"fit_outlier_bounds ✅ Method: {method.upper()}")
    return bounds

# 2. Remove outliers based on bounds
def remove_outliers(df: pd.DataFrame, bounds: dict) -> pd.DataFrame:
    df_cleaned = df.copy()
    for col, (lower, upper) in bounds.items():
        before_count = df_cleaned.shape[0]
        df_cleaned = df_cleaned[(df_cleaned[col] >= lower) & (df_cleaned[col] <= upper)]
        after_count = df_cleaned.shape[0]
        print(f"remove_outliers ✅ {col}: Removed {before_count - after_count} rows")
    return df_cleaned

# 3. Cap outliers instead of removing
def cap_outliers(df: pd.DataFrame, bounds: dict) -> pd.DataFrame:
    df_capped = df.copy()
    for col, (lower, upper) in bounds.items():
        df_capped[col] = df_capped[col].clip(lower, upper)
        print(f"cap_outliers ✅ {col}: Values capped to range ({lower}, {upper})")
    return df_capped

# 4. Dynamic decision logic: auto-cap or auto-remove
def adaptive_outlier_handling(df: pd.DataFrame, method: str = "iqr", strategy: str = "auto") -> pd.DataFrame:
    bounds = fit_outlier_bounds(df, method=method)
    row_count = df.shape[0]

    if strategy == "auto":
        strategy = "cap" if row_count <= 1000 else "remove"
        print(f"adaptive_outlier_handling 🚦 Auto-selected strategy: {strategy.upper()}")

    if strategy == "cap":
        return cap_outliers(df, bounds)
    elif strategy == "remove":
        return remove_outliers(df, bounds)
    else:
        raise ValueError("Invalid strategy. Choose from: 'cap', 'remove', or 'auto'")

# 5. Optional visualization for debugging
def visualize_outliers(df: pd.DataFrame, method: str = "iqr", columns: list = None, z_thresh: float = 3.0, iqr_multiplier: float = 1.5):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    columns = columns or numeric_cols

    for col in columns:
        if col not in df.columns:
            print(f"⚠️ Column '{col}' not in DataFrame.")
            continue

        col_data = df[col].dropna()
        plt.figure(figsize=(14, 5))

        # Calculate bounds
        if method == "zscore":
            mean = col_data.mean()
            std = col_data.std()
            lower = mean - z_thresh * std
            upper = mean + z_thresh * std

        elif method == "iqr":
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - iqr_multiplier * IQR
            upper = Q3 + iqr_multiplier * IQR

        else:
            raise ValueError("Method must be 'zscore' or 'iqr'")

        # Boxplot
        plt.subplot(1, 2, 1)
        sns.boxplot(x=col_data, color="lightblue")
        plt.axvline(lower, color='red', linestyle='--', label='Lower Bound')
        plt.axvline(upper, color='green', linestyle='--', label='Upper Bound')
        plt.title(f"Boxplot for '{col}'")
        plt.legend()

        # Histogram
        plt.subplot(1, 2, 2)
        sns.histplot(col_data, kde=True, color="lightgray")
        plt.axvline(lower, color='red', linestyle='--', label='Lower Bound')
        plt.axvline(upper, color='green', linestyle='--', label='Upper Bound')
        plt.title(f"Histogram for '{col}'")
        plt.legend()

        plt.suptitle(f"Outlier Visualization - {col} ({method.upper()})")
        plt.tight_layout()
        plt.show()