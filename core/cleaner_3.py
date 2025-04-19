import re
import pandas as pd                                      # type:ignore
from core.detector_2 import detection

class Cleaning:
    def remove_special_characters(self, dataframe: pd.DataFrame):
        """Remove special characters from column names only."""
        dataframe.columns = dataframe.columns.str.replace(r'[^a-zA-Z0-9_]', ' ',  regex=True)
        print("remove_special_characters_from_columns ✅")
        return dataframe

    def convert_to_lowercase(self, dataframe: pd.DataFrame):
        """Convert column names to lowercase only."""
        dataframe.columns = dataframe.columns.str.lower()
        print("convert_column_names_to_lowercase ✅")
        return dataframe

    def remove_whitespace(self, dataframe: pd.DataFrame):
        """Remove leading/trailing whitespace from column names only."""
        dataframe.columns = dataframe.columns.str.strip()
        print("remove_whitespace_from_column_names ✅")
        return dataframe

    def replace_space_with_underscore(self, dataframe: pd.DataFrame):
        """Replace spaces with underscores in column names only."""
        dataframe.columns = dataframe.columns.str.replace(' ', '_', regex=False)
        print("replace_space_with_underscore_in_columns ✅")
        return dataframe

    def remove_empty_columns(self, dataframe: pd.DataFrame):
        dataframe = dataframe.dropna(axis=1, how='all')
        print("remove_empty_columns ✅")
        return dataframe

    def remove_empty_rows(self, dataframe: pd.DataFrame):
        dataframe = dataframe.dropna(axis=0, how='all')
        print("remove_empty_rows ✅")
        return dataframe

    def identifier_column_remover(self, dataframe: pd.DataFrame, identifier_keywords: list = ['id', 'identifier']):
        _, column_types = detection(dataframe)
        columns_to_drop = [
            column for column in dataframe.columns
            if any(keyword in column.lower() for keyword in identifier_keywords) and column_types.get(column) in ['int', 'str']
        ]

        # Additional logic to identify integer columns with unique, increasing values
        for column in dataframe.columns:
            if column_types.get(column) == 'int':
                if dataframe[column].is_unique and dataframe[column].is_monotonic_increasing:
                    columns_to_drop.append(column)

        dataframe = dataframe.drop(columns=columns_to_drop)
        print("identifier_column_remover ✅")
        return dataframe

    def remove_duplicates(self, dataframe: pd.DataFrame):
        dataframe = dataframe.drop_duplicates().reset_index(drop=True)
        print("remove_duplicates ✅")
        return dataframe        