# >--Encoder.py--<

from sklearn.preprocessing import LabelEncoder

def fit_label_encoders(df, columns=None):
    encoders = {}
    if columns is None:
        columns = df.select_dtypes(include='object').columns

    for col in columns:
        le = LabelEncoder()
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        print(f"🔤 LabelEncoder fitted on '{col}'")

    return df, encoders

def transform_label_encoders(df, encoders):
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = le.transform(df[col])
            print(f"🔁 Transformed '{col}' using LabelEncoder")
    return df

from sklearn.preprocessing import OneHotEncoder

def fit_onehot_encoders(df, columns=None):
    if columns is None:
        columns = df.select_dtypes(include='object').columns

    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    ohe.fit(df[columns])
    print(f"🧩 OneHotEncoder fitted on: {columns}")
    return ohe

def transform_onehot_encoders(df, ohe, columns=None):
    if columns is None:
        columns = df.select_dtypes(include='object').columns

    encoded = ohe.transform(df[columns])
    ohe_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out(columns), index=df.index)

    df = df.drop(columns=columns)
    df = pd.concat([df, ohe_df], axis=1)
    print(f"🔁 OneHotEncoder applied. Added {len(ohe_df.columns)} columns.")
    return df

from sklearn.preprocessing import OrdinalEncoder

def fit_ordinal_encoders(df, columns_with_order: dict):
    """
    columns_with_order: dict like {'education': ['high school', 'bachelor', 'master', 'phd']}
    """
    oe = OrdinalEncoder(categories=[columns_with_order[col] for col in columns_with_order])
    cols = list(columns_with_order.keys())
    oe.fit(df[cols])
    print(f"🔢 OrdinalEncoder fitted on: {cols}")
    return oe, cols

def transform_ordinal_encoders(df, oe, columns):
    df[columns] = oe.transform(df[columns])
    print(f"🔁 OrdinalEncoder applied on {columns}")
    return df

def frequency_encoder(df, columns=None):
    """
    Replace categories with their frequency count or proportion.
    """
    if columns is None:
        columns = df.select_dtypes(include='object').columns

    for col in columns:
        freq = df[col].value_counts(normalize=True)
        df[col] = df[col].map(freq)
        print(f"📊 Frequency encoding applied on '{col}'")
    
    return df

def encode_all(df):
    df, label_encoders = fit_label_encoders(df)
    df = frequency_encoder(df)
    return df, label_encoders

-------------------------------------------------------------
