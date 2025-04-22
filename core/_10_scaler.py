
# Scaler.py

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def fit_scaler(X, scaler_type="standard"):
    """
    Fit a scaler to the features of the dataset.
    
    Args:
    - X (DataFrame): Feature matrix to scale
    - scaler_type (str): The type of scaler to use. Options: 'standard', 'minmax', 'robust'
    
    Returns:
    - scaler (object): The fitted scaler
    """
    if scaler_type == "standard":
        scaler = StandardScaler()
    elif scaler_type == "minmax":
        scaler = MinMaxScaler()
    elif scaler_type == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unsupported scaler type: {scaler_type}")
    
    scaler.fit(X)
    print(f"✅ Fitted {scaler_type} scaler")
    return scaler

def transform_scaler(X, scaler):
    """
    Transform the feature matrix using the fitted scaler.
    
    Args:
    - X (DataFrame): Feature matrix to scale
    - scaler (object): The fitted scaler (StandardScaler, MinMaxScaler, etc.)
    
    Returns:
    - X_scaled (DataFrame): The scaled feature matrix
    """
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    print(f"✅ Scaled features using {scaler.__class__.__name__}")
    return X_scaled_df

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_scaling_effect(X, X_scaled):
    """
    Visualize the effect of scaling on feature distributions using histograms.
    
    Args:
    - X (DataFrame): Original feature matrix
    - X_scaled (DataFrame): Scaled feature matrix
    
    Returns:
    - None: Plots histograms of the original vs scaled features
    """
    num_features = X.shape[1]
    
    # Set up subplots
    fig, axes = plt.subplots(nrows=num_features, ncols=2, figsize=(10, num_features*3))
    
    for i, column in enumerate(X.columns):
        # Original feature distribution
        axes[i, 0].hist(X[column], bins=20, color='skyblue', edgecolor='black')
        axes[i, 0].set_title(f'Original: {column}')
        
        # Scaled feature distribution
        axes[i, 1].hist(X_scaled[column], bins=20, color='lightgreen', edgecolor='black')
        axes[i, 1].set_title(f'Scaled: {column}')
    
    plt.tight_layout()
    plt.show()
    print("✅ Visualization of feature distributions before and after scaling.")

# Example usage
# Assume you have a DataFrame `df` with feature columns

X = df.drop('target', axis=1)  # Features
y = df['target']  # Target (not scaled)

# Fit scaler (StandardScaler)
scaler = fit_scaler(X, scaler_type="standard")

# Transform the features using the fitted scaler
X_scaled = transform_scaler(X, scaler)

# Visualize the effect of scaling
visualize_scaling_effect(X, X_scaled)

# 💡 Notes and Tips:
# StandardScaler: Subtracts the mean and divides 
# by the standard deviation. Good for data that
# follows a Gaussian distribution.
# MinMaxScaler: Scales data between a specified
#  range, typically between 0 and 1. Useful when 
# the range of data needs to be normalized.
# RobustScaler: Uses the median and interquartile 
# range for scaling, which is more robust to outliers 
# compared to StandardScaler and MinMaxScaler.

# 💡 Visualization of scaling effects:
# The visualize_scaling_effect() function helps you 
# compare the original feature distributions with 
# the scaled ones, so you can check how well the 
# scaling has worked.
# This can be very useful when dealing with datasets 
# that contain highly skewed distributions or outliers.

-------------------------------------------------------------
