import pandas as pd                      

class cleaning:
    def standardize_empty_cells(self, dataframe: pd.DataFrame):
        """Standardize all variations of empty cells to pd.NA for consistency."""
        dataframe = dataframe.applymap(lambda x: pd.NA if pd.isna(x) else x)
        print("standardize_empty_cells")
        return dataframe

    def remove_special_characters(self, dataframe: pd.DataFrame):
        """Remove special characters from column names only."""
        dataframe.columns = dataframe.columns.str.replace(r'[^a-zA-Z0-9_]', ' ',  regex=True)
        print("remove_special_characters_from_columns")
        return dataframe

    def convert_to_lowercase(self, dataframe: pd.DataFrame):
        """Convert column names to lowercase only."""
        dataframe.columns = dataframe.columns.str.lower()
        print("convert_column_names_to_lowercase")
        return dataframe

    def remove_whitespace(self, dataframe: pd.DataFrame):
        """Remove leading/trailing whitespace from column names only."""
        dataframe.columns = dataframe.columns.str.strip()
        print("remove_whitespace_from_column_names")
        return dataframe

    def replace_space_with_underscore(self, dataframe: pd.DataFrame):
        """Replace spaces with underscores in column names only."""
        dataframe.columns = dataframe.columns.str.replace(' ', '_', regex=False)
        print("replace_space_with_underscore_in_columns")
        return dataframe

    def remove_empty_columns(self, dataframe: pd.DataFrame):
        dataframe = dataframe.dropna(axis=1, how='all')
        print("remove_empty_columns")
        return dataframe

    def remove_empty_rows(self, dataframe: pd.DataFrame):
        """Remove rows where all values are missing, considering all representations of missing values."""
        dataframe = dataframe.loc[~dataframe.isnull().all(axis=1)]
        print("remove_empty_rows")
        return dataframe

    def identifier_column_remover(self, dataframe: pd.DataFrame):
        columns_to_drop = []

        # Logic to identify integer columns with unique, increasing values
        for column in dataframe.columns:
            if dataframe[column].dtype == 'int' and dataframe[column].is_unique and dataframe[column].is_monotonic_increasing:
                columns_to_drop.append(column)

        dataframe = dataframe.drop(columns=columns_to_drop)
        print("identifier_column_remover")
        return dataframe

    def remove_duplicates(self, dataframe: pd.DataFrame):
        dataframe = dataframe.drop_duplicates().reset_index(drop=True)
        print("remove_duplicates")
        return dataframe

    def run_cleaning(self, dataframe: pd.DataFrame):
        """Apply all cleaning methods in sequence to the DataFrame."""
        dataframe = self.standardize_empty_cells(dataframe)
        dataframe = self.remove_special_characters(dataframe)
        dataframe = self.convert_to_lowercase(dataframe)
        dataframe = self.remove_whitespace(dataframe)
        dataframe = self.replace_space_with_underscore(dataframe)
        dataframe = self.identifier_column_remover(dataframe)
        dataframe = self.remove_empty_columns(dataframe)
        dataframe = self.remove_empty_rows(dataframe)
        dataframe = self.remove_duplicates(dataframe)
        print("All cleaning methods applied successfully.")
        return dataframe