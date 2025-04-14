import re
import pandas as pd
from dateutil.parser import parse

def detection(dataframe):
    """
    Detects the datatype of each column in the dataframe and returns the dataframe along with detected column types.
    """
    column_types = {}
    time_pattern = re.compile(r'\d{2}:\d{2}:\d{2}')  # Example: 14:30:00

    for column in dataframe.columns:
        dtype = dataframe[column].dtype
        if pd.api.types.is_integer_dtype(dtype):
            column_types[column] = 'int'
        elif pd.api.types.is_float_dtype(dtype):
            column_types[column] = 'float'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            column_types[column] = 'datetime'
        elif pd.api.types.is_bool_dtype(dtype):
            column_types[column] = 'bool'
        elif pd.api.types.is_string_dtype(dtype):
            try:
                if dataframe[column].apply(lambda x: bool(parse(str(x), fuzzy=False))).all():
                    column_types[column] = 'date'
                elif dataframe[column].astype(str).str.match(time_pattern).all():
                    column_types[column] = 'time'
                else:
                    column_types[column] = 'str'
            except Exception:
                column_types[column] = 'str'
        else:
            column_types[column] = 'unknown'

    return dataframe, column_types