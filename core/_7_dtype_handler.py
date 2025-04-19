# Datatype_correction.py

def enforce_column_types(df: pd.DataFrame, type_map: dict):
    """
    Force column types based on a given type mapping dictionary.
    Example: {"age": int, "salary": float, "joined": "datetime64[ns]"}
    """
    for col, expected_type in type_map.items():
        if col not in df.columns:
            print(f"⚠️ Column '{col}' not found. Skipping.")
            continue

        try:
            df[col] = df[col].astype(expected_type)
            print(f"✅ '{col}' converted to {expected_type}")
        except Exception as e:
            print(f"❌ Could not convert '{col}' to {expected_type}: {e}")

    return df

def convert_types_as_needed(df: pd.DataFrame):
    """
    Tries to automatically convert object types into more specific ones like int, float, bool, or datetime.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try numeric conversion
            try:
                converted = pd.to_numeric(df[col], errors='coerce')
                if converted.notna().sum() >= len(df) * 0.8:
                    df[col] = converted
                    print(f"🔢 Converted '{col}' to numeric")
                    continue
            except:
                pass

            # Try datetime conversion
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().sum() >= len(df) * 0.8:
                    df[col] = converted
                    print(f"🗓️ Converted '{col}' to datetime")
                    continue
            except:
                pass

            # Try boolean conversion
            if df[col].dropna().str.lower().isin(['true', 'false', 'yes', 'no']).all():
                df[col] = df[col].str.lower().map({'true': True, 'false': False, 'yes': True, 'no': False})
                print(f"✅ Converted '{col}' to boolean")
    
    return df

from dateutil.parser import parse
import re

def detect_types_proactively(df: pd.DataFrame, sample_size: int = 10):
    """
    Predict column types from a few top rows. Returns a dict: {column: predicted_type}
    Useful for early validation or logging before final cleanup.
    """
    predicted_types = {}
    time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")

    for col in df.columns:
        sample = df[col].dropna().astype(str).head(sample_size).str.strip()

        # Boolean check
        if sample.str.lower().isin(['true', 'false', 'yes', 'no']).all():
            predicted_types[col] = 'bool'
            continue

        # Time check
        if sample.str.match(time_pattern).all():
            predicted_types[col] = 'time'
            continue

        # Date check
        date_count = 0
        for val in sample:
            try:
                parse(val, fuzzy=False, dayfirst=True)
                date_count += 1
            except:
                pass
        if date_count >= len(sample) * 0.8:
            predicted_types[col] = 'date'
            continue

        # Numeric check
        numeric_sample = pd.to_numeric(sample, errors='coerce')
        if numeric_sample.notna().all():
            if all(float(x).is_integer() for x in numeric_sample):
                predicted_types[col] = 'int'
            else:
                predicted_types[col] = 'float'
            continue

        predicted_types[col] = 'str'

    return predicted_types


# Predict types before applying conversions
predicted = detect_types_proactively(df)
print(predicted)

# Force specific column types (from config or manual mapping)
type_map = {"age": int, "salary": float, "joined": "datetime64[ns]"}
df = enforce_column_types(df, type_map)

# Optional: auto-convert wherever needed
df = convert_types_as_needed(df)
