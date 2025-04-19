# >--feature_selector.py--<

from sklearn.feature_selection import RFE, SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression

def fit_feature_selector(X, y, method="rfe", estimator=None, k="all"):
    """
    Fit feature selector based on the method.
    
    - RFE (Recursive Feature Elimination)
    - SelectKBest with ANOVA F-test
    
    Args:
    - X (DataFrame): Feature matrix
    - y (Series): Target variable
    - method (str): Feature selection method, either 'rfe' or 'selectkbest'
    - estimator (model object): Estimator to use for RFE (default LogisticRegression)
    - k (int or "all"): Number of features to select (default 'all')
    
    Returns:
    - selected_features (list): List of selected feature names
    """
    if estimator is None:
        estimator = LogisticRegression()  # Default estimator if none is provided
    
    if method == "rfe":
        selector = RFE(estimator, n_features_to_select=k)
        selector = selector.fit(X, y)
    elif method == "selectkbest":
        selector = SelectKBest(score_func=f_classif, k=k)
        selector = selector.fit(X, y)
    else:
        raise ValueError(f"Unknown method: {method}")

    selected_features = X.columns[selector.support_].tolist()
    print(f"✅ Selected Features: {selected_features}")
    return selected_features

def drop_selected_features(X, selected_features):
    """
    Drop the selected features from the dataframe.
    
    Args:
    - X (DataFrame): Feature matrix
    - selected_features (list): List of features to drop
    
    Returns:
    - X_dropped (DataFrame): DataFrame with the selected features dropped
    """
    X_dropped = X.drop(columns=selected_features)
    print(f"✅ Dropped Features: {selected_features}")
    return X_dropped

from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt

def auto_feature_importance(X, y, model_type="random_forest", top_n=10):
    """
    Automatically rank and plot feature importances using models like RandomForest or XGBoost.
    
    Args:
    - X (DataFrame): Feature matrix
    - y (Series): Target variable
    - model_type (str): Model to use for ranking features, either 'random_forest' or 'xgboost'
    - top_n (int): Number of top features to return
    
    Returns:
    - feature_importance_df (DataFrame): Features ranked by importance
    """
    if model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == "xgboost":
        model = xgb.XGBClassifier(n_estimators=100, random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(X, y)
    
    # Get feature importances
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': feature_importances
    })
    
    # Sort by importance
    feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
    
    # Plot top N features
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df.head(top_n)['feature'], feature_importance_df.head(top_n)['importance'])
    plt.xlabel('Feature Importance')
    plt.title(f'Top {top_n} Feature Importances')
    plt.gca().invert_yaxis()
    plt.show()

    return feature_importance_df

# Example usage
X = df.drop('target', axis=1)
y = df['target']

# Fit Feature Selector
selected_features = fit_feature_selector(X, y, method="rfe", k=5)

# Drop the selected features
X_dropped = drop_selected_features(X, selected_features)

# Auto-Feature Importance using RandomForest
feature_importance_df = auto_feature_importance(X, y, model_type="random_forest", top_n=10)

print("Feature Importance Rankings:")
print(feature_importance_df.head(10))

# Extra Tips:
# Use RandomForest or XGBoost when dealing with large 
# datasets to automatically detect important features.
# Recursive Feature Elimination (RFE) is useful when 
# you need a more controlled selection based on model performance.
# SelectKBest is a simpler method based on univariate 
# feature selection that can work well with small datasets.

--------------------------------------------------------
