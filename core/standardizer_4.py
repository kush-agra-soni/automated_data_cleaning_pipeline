def standardize_numerical_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes commas, %, $, and converts to proper numeric type if needed.
    """
    for col in df.select_dtypes(include='object').columns:
        try:
            df[col] = df[col].str.replace(r'[,\$%]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except Exception as e:
            print(f"Error cleaning numeric format in {col}: {e}")
    print("standardize_numerical_format ✅")
    return df

def standardize_string_format(df: pd.DataFrame):
    """
    Trims, lowers, and removes extra spaces from all string columns.
    """
    object_cols = df.select_dtypes(include='object').columns

    for col in object_cols:
        df[col] = df[col].astype(str) \
                         .str.strip() \
                         .str.lower() \
                         .str.replace(r'\s+', ' ', regex=True)
        print(f"🔤 Standardized string format in '{col}'")

    return df

def standardize_date_format(df: pd.DataFrame, date_columns: list = None, output_format: str = "%Y-%m-%d"):
    """
    Standardizes date columns to a uniform format (e.g., YYYY-MM-DD).
    You can specify which columns to convert, or it'll try all object columns.
    """
    if date_columns is None:
        date_columns = df.select_dtypes(include='object').columns

    for col in date_columns:
        try:
            parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            if parsed.notna().sum() >= len(df) * 0.5:
                df[col] = parsed.dt.strftime(output_format)
                print(f"📆 Standardized date format in '{col}'")
        except Exception as e:
            print(f"❌ Could not format '{col}': {e}")
    
    return df

def standardize_units(df: pd.DataFrame, unit_map: dict):
    """
    Converts different representations of units to a standard unit based on mapping.
    Example: {'kg': ['kilogram', 'kgs', 'kg.', 'kilograms']}
    """
    for col in df.select_dtypes(include='object').columns:
        for standard_unit, variants in unit_map.items():
            df[col] = df[col].str.lower().replace(variants, standard_unit, regex=True)
    
    print("⚖️ Standardized unit representations.")
    return df

unit_map = {
    'kg': [r'\bkilograms?\b', r'\bkgs?\b', r'\bkg\.\b'],
    'usd': [r'\$|usd|us dollars?'],
}

def standardize_boolean_format(df: pd.DataFrame):
    """
    Converts yes/no, true/false, y/n, etc., into Python boolean values.
    """
    true_values = ['true', 'yes', 'y', '1']
    false_values = ['false', 'no', 'n', '0']

    for col in df.select_dtypes(include='object').columns:
        lowercase_col = df[col].astype(str).str.lower().str.strip()
        if lowercase_col.isin(true_values + false_values).all():
            df[col] = lowercase_col.map(lambda x: True if x in true_values else False)
            print(f"✅ Standardized boolean format in '{col}'")
    
    return df

def format_all(df: pd.DataFrame, unit_map: dict = None):
    df = standardize_numerical_format(df)
    df = standardize_string_format(df)
    df = standardize_date_format(df)
    df = standardize_units(df, unit_map or {})
    df = standardize_boolean_format(df)
    if unit_map:
        df = standardize_units(df, unit_map)
    return df

