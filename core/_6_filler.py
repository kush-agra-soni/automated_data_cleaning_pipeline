# >--missing_value_handling--<

from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import warnings

def _regression_impute(df: pd.DataFrame, target_col: str, model, categorical=False):
    """
    Uses regression model to impute missing values for target_col.
    Supports both linear and logistic (categorical=True).
    """
    df = df.copy()
    cols = [c for c in df.columns if c != target_col and df[c].notna().all()]
    if not cols:
        raise ValueError(f"No complete columns available to use as predictors for '{target_col}'.")

    complete_rows = df[df[target_col].notna()]
    missing_rows = df[df[target_col].isna()]

    X_train = complete_rows[cols]
    y_train = complete_rows[target_col]
    X_test = missing_rows[cols]

    if categorical:
        # Convert categorical target to numeric
        mapping = {k: i for i, k in enumerate(y_train.dropna().unique())}
        y_train = y_train.map(mapping)
        model = make_pipeline(StandardScaler(), model)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        inv_map = {v: k for k, v in mapping.items()}
        df.loc[df[target_col].isna(), target_col] = [inv_map.get(int(round(x)), np.nan) for x in pred]
    else:
        model = make_pipeline(StandardScaler(), model)
        try:
            model.fit(X_train, np.log1p(y_train))
            pred = np.expm1(model.predict(X_test))
        except:
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
        df.loc[df[target_col].isna(), target_col] = pred

    return df


def impute_missing_values(self, df: pd.DataFrame, strategy: str = 'mean', n_neighbors: int = 3):
    """
    Fills missing values using various strategies:
    'mean', 'median', 'mode', 'knn', 'linreg', 'logreg', 'auto'

    Auto Strategy:
    - numeric → linreg → knn
    - categorical → logreg → knn

    Args:
        df: pandas DataFrame
        strategy: imputation method
        n_neighbors: used for knn strategy
    Returns:
        df: DataFrame with imputed values
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(exclude=['number']).columns

    if strategy in ['mean', 'median', 'mode']:
        for col in df.columns:
            if df[col].isna().any():
                if col in numeric_cols:
                    if strategy == 'mean':
                        value = df[col].mean()
                    elif strategy == 'median':
                        value = df[col].median()
                    else:
                        value = df[col].mode()[0]
                else:
                    value = df[col].mode()[0]
                df[col] = df[col].fillna(value)
        print(f"impute_missing_values ({strategy}) ✅")

    elif strategy == 'knn':
        imputer = KNNImputer(n_neighbors=n_neighbors)
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
        print("impute_missing_values (knn) ✅")

    elif strategy == 'linreg':
        for col in numeric_cols:
            if df[col].isna().sum() > 0:
                df = _regression_impute(df, col, model=LinearRegression())
        print("impute_missing_values (linreg) ✅")

    elif strategy == 'logreg':
        for col in categorical_cols:
            if df[col].isna().sum() > 0:
                df = _regression_impute(df, col, model=LogisticRegression(), categorical=True)
        print("impute_missing_values (logreg) ✅")

    elif strategy == 'auto':
        # numeric
        for col in numeric_cols:
            if df[col].isna().sum() > 0:
                try:
                    df = _regression_impute(df, col, model=LinearRegression())
                except:
                    try:
                        imputer = KNNImputer(n_neighbors=n_neighbors)
                        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                        print(f"Auto fallback to KNN for {col}")
                    except:
                        warnings.warn(f"Auto strategy failed for numeric col: {col}")

        # categorical
        for col in categorical_cols:
            if df[col].isna().sum() > 0:
                try:
                    df = _regression_impute(df, col, model=LogisticRegression(), categorical=True)
                except:
                    warnings.warn(f"Auto strategy failed for categorical col: {col}")

        print("impute_missing_values (auto) ✅")

    else:
        raise ValueError("Invalid strategy. Choose from 'mean', 'median', 'mode', 'knn', 'linreg', 'logreg', 'auto'.")

    return df


# ---------------------------------------------------------
#################### Date Extraction ######################
# ---------------------------------------------------------

def extract_dates(self, dataframe: pd.DataFrame, date_format: str = None):
    time_only_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')

    for column in dataframe.select_dtypes(include=['object']).columns:
        try:
            # Check if it's a time-only column based on the first few values
            sample = dataframe[column].dropna().astype(str).head(5)
            if sample.str.match(time_only_pattern).all():
                continue  # Skip time-only columns

            # Parse potential date columns
            parsed_dates = pd.to_datetime(dataframe[column], errors='coerce', format=date_format)

            # Only extract if parsing is somewhat successful
            if not parsed_dates.isna().all():
                dataframe[f"{column}_day"] = parsed_dates.dt.day
                dataframe[f"{column}_month"] = parsed_dates.dt.month
                dataframe[f"{column}_year"] = parsed_dates.dt.year

        except Exception as e:
            print(f"Error processing column {column}: {e}")

    return dataframe

