import re
import pandas as pd                # type:ignore
from dateutil.parser import parse  # type:ignore

def detection(dataframe):
    column_types = {}
    time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')  # HH:MM:SS format

    for column in dataframe.columns:
        non_nan_values = dataframe[column].dropna().head(10)

        if non_nan_values.empty:
            column_types[column] = 'unknown'
            continue

        str_values = non_nan_values.astype(str).str.strip()

        # 1. Detect boolean-like strings
        if str_values.str.lower().isin(['true', 'false']).all():
            column_types[column] = 'bool'
            continue

        # 2. Detect time
        if str_values.str.match(time_pattern).all():
            column_types[column] = 'time'
            continue

        # 3. Detect strictly formatted dates (dd-mm-yy or yyyy-mm-dd)
        date_like_count = 0
        for val in str_values:
            try:
                parsed = parse(val, fuzzy=False, dayfirst=True)
                # Count only if original string has '-' or '/' to avoid numeric misclassification
                if any(sep in val for sep in ['-', '/']):
                    date_like_count += 1
            except Exception:
                pass
        if date_like_count == len(str_values):
            column_types[column] = 'date'
            continue

        # 4. Detect numeric (and separate int vs float)
        try:
            numeric_values = pd.to_numeric(str_values, errors='coerce')
            if numeric_values.notna().all():
                if (numeric_values % 1 == 0).all():
                    column_types[column] = 'int'
                else:
                    column_types[column] = 'float'
                continue
        except Exception:
            pass

        # 5. Fallback to string
        column_types[column] = 'str'

    return dataframe, column_types


