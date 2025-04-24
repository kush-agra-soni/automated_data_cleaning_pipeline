import re
import pandas as pd                
from dateutil.parser import parse 

class datadetector:
    def __init__(self):
        self.time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')  # HH:MM:SS format

    def detect_time_column(self, dataframe):
        """Detect columns with time format (xx:xx:xx) and typecast them as time-only."""
        for column in dataframe.columns:
            str_values = dataframe[column].dropna().astype(str).str.strip()
            if str_values.str.match(self.time_pattern).all():
                dataframe[column] = pd.to_datetime(dataframe[column], format='%H:%M:%S', errors='coerce').dt.time
                dataframe[column] = dataframe[column].astype('string')  # Ensure dtype is string to avoid showing dates
                print(f"Column '{column}' detected as time and typecasted to time-only.")
        return dataframe

    def detect_column_type(self, dataframe, column):
        """Detect the type of a single column."""
        str_values = dataframe[column].dropna().astype(str).str.strip()

        # Detect boolean-like strings
        if str_values.str.lower().isin(['true', 'false', 'yes', 'no', '1', '0']).all():
            dataframe[column] = str_values.str.lower().map(lambda x: True if x in ['true', 'yes', '1'] else False)
            return 'bool'

        # Detect strictly formatted dates
        if all(any(sep in val for sep in ['-', '/']) and self.is_date(val) for val in str_values):
            dataframe[column] = pd.to_datetime(dataframe[column], errors='coerce')
            return 'date'

        # Detect numeric (and separate int vs float)
        numeric_values = pd.to_numeric(str_values, errors='coerce')
        if numeric_values.notna().all():
            if (numeric_values % 1 == 0).all():
                dataframe[column] = numeric_values.astype('Int64')
                return 'int'
            dataframe[column] = numeric_values.astype('float')
            return 'float'

        # Fallback to string
        dataframe[column] = dataframe[column].astype(str)
        return 'str'

    @staticmethod
    def is_date(value):
        """Check if a value is a valid date."""
        try:
            parse(value, fuzzy=False, dayfirst=True)
            return True
        except Exception:
            return False

    def detect_column_types(self, dataframe):
        """Detect types for all columns in the dataframe."""
        column_types = {}
        for column in dataframe.columns:
            if dataframe[column].dropna().empty:
                column_types[column] = 'unknown'
            else:
                column_types[column] = self.detect_column_type(dataframe, column)
        return dataframe, column_types

    def detection(self, dataframe):
        dataframe = self.detect_time_column(dataframe)
        dataframe, column_types = self.detect_column_types(dataframe)
        print(dataframe.info())
        return dataframe, column_types