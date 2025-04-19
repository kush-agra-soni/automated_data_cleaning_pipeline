# >--validator.py--<

def check_final_nans(df):
    """
    Check for missing values (NaN) in the dataset.
    
    Args:
    - df (DataFrame): The DataFrame to check
    
    Returns:
    - None: Prints out columns with NaNs
    """
    nan_summary = df.isna().sum()
    nan_columns = nan_summary[nan_summary > 0]
    
    if not nan_columns.empty:
        print(f"✅ Columns with missing values (NaNs):\n{nan_columns}")
    else:
        print("✅ No missing values found.")

def check_invalid_types(df):
    """
    Check for invalid or unexpected data types in the dataset.
    
    Args:
    - df (DataFrame): The DataFrame to check
    
    Returns:
    - None: Prints out columns with invalid types
    """
    invalid_columns = df.select_dtypes(exclude=['number']).columns
    
    if len(invalid_columns) > 0:
        print(f"✅ Columns with invalid data types:\n{invalid_columns}")
    else:
        print("✅ All columns have valid data types.")

import numpy as np
from scipy import stats

def recheck_outliers(df, method="zscore", threshold=3):
    """
    Recheck for outliers in the dataset using Z-scores or IQR method.
    
    Args:
    - df (DataFrame): The DataFrame to check
    - method (str): Method to use for outlier detection. Options: 'zscore', 'iqr'
    - threshold (float): The threshold value for outlier detection (default is 3)
    
    Returns:
    - None: Prints out columns with detected outliers
    """
    if method == "zscore":
        z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
        outliers = (z_scores > threshold).sum(axis=0)
        
        outlier_columns = outliers[outliers > 0]
        if len(outlier_columns) > 0:
            print(f"✅ Columns with Z-score outliers:\n{outlier_columns}")
        else:
            print("✅ No Z-score outliers found.")
    
    elif method == "iqr":
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum(axis=0)
        
        outlier_columns = outliers[outliers > 0]
        if len(outlier_columns) > 0:
            print(f"✅ Columns with IQR outliers:\n{outlier_columns}")
        else:
            print("✅ No IQR outliers found.")
    
    else:
        raise ValueError("Invalid method. Choose either 'zscore' or 'iqr'.")

import seaborn as sns
import matplotlib.pyplot as plt

def visualize_data_distribution(df):
    """
    Visualize the distribution of features in the dataset using histograms, KDEs, and boxplots.
    
    Args:
    - df (DataFrame): The DataFrame to visualize
    
    Returns:
    - None: Displays the plots
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    fig, axes = plt.subplots(nrows=len(numeric_columns), ncols=3, figsize=(15, len(numeric_columns) * 5))
    
    for i, column in enumerate(numeric_columns):
        # Histogram
        sns.histplot(df[column], kde=False, ax=axes[i, 0], color='skyblue')
        axes[i, 0].set_title(f'Histogram of {column}')
        
        # KDE plot
        sns.kdeplot(df[column], ax=axes[i, 1], color='green')
        axes[i, 1].set_title(f'KDE of {column}')
        
        # Boxplot
        sns.boxplot(x=df[column], ax=axes[i, 2], color='orange')
        axes[i, 2].set_title(f'Boxplot of {column}')
    
    plt.tight_layout()
    plt.show()
    print("✅ Visualized data distributions using histograms, KDE, and boxplots.")

# Example usage
# Assume you have a DataFrame `df`

# Check for missing values (NaNs)
check_final_nans(df)

# Check for invalid data types
check_invalid_types(df)

# Recheck for outliers using Z-scores
recheck_outliers(df, method="zscore", threshold=3)

# Visualize the data distribution
visualize_data_distribution(df)