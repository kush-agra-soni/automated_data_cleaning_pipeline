import pandas as pd

class standardizer:
    def __init__(self, unit_map=None):
        self.unit_map = unit_map or {
            'kg': [r'\bkilograms?\b', r'\bkgs?\b', r'\bkg\.\b'],
            'usd': [r'\$|usd|us dollars?']
        }

    def standardize_numerical_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes commas, %, $, and converts to proper numeric type if needed.
        """
        numeric_columns = [col for col in df.select_dtypes(include=['int', 'float']).columns]
        float_columns = [col for col in df.select_dtypes(include=['float']).columns]  # Define float columns

        for col in numeric_columns:
            try:
                if df[col].dtype == 'object':  # Ensure column is string before applying .str
                    df[col] = df[col].str.extract(r'(\d+)')[0]  # Extract numeric part from string
                if col in float_columns:  # Round float columns to one decimal place
                    df[col] = pd.to_numeric(df[col], errors='coerce').round(1)
                else:  # Convert other numeric columns to integers
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            except Exception as e:
                print(f"Error cleaning numeric format in {col}: {e}")

        # Process all string columns to extract numeric values if present
        string_columns = [col for col in df.select_dtypes(include=['object']).columns]

        for col in string_columns:
            try:
                # Check if the column contains any numeric values
                if df[col].str.contains(r'\d', regex=True, na=False).any():
                    # Extract numeric part from string
                    df[col] = df[col].str.extract(r'(\d+\.\d+|\d+)')[0]
                    # Convert to float if decimals are present, otherwise to int
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                else:
                    # Leave the column as string if no numeric values are found
                    df[col] = df[col].astype(str)
            except Exception as e:
                print(f"Error processing column {col}: {e}")

        print("standardize_numerical_format ✅")
        return df

    def standardize_string_format(self, df: pd.DataFrame):
        """
        Trims, lowers, and removes extra spaces from all string columns.
        """
        string_columns = [col for col in df.select_dtypes(include=['object']).columns]

        for col in string_columns:
            df[col] = df[col].astype(str) \
                             .str.strip() \
                             .str.lower() \
                             .str.replace(r'\s+', ' ', regex=True)
            print(f"🔤 Standardized string format in '{col}'")

        return df

    def standardize_date_format(self, df: pd.DataFrame, output_format: str = "%Y-%m-%d"):
        """
        Standardizes date columns to a uniform format (e.g., YYYY-MM-DD).
        """
        date_columns = [col for col in df.select_dtypes(include=['datetime']).columns]

        for col in date_columns:
            try:
                # Attempt to parse dates with dayfirst=True for ambiguous formats
                parsed = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                if parsed.notna().sum() >= len(df) * 0.5:  # Ensure at least 50% valid dates
                    df[col] = parsed.dt.strftime(output_format)  # Standardize to ISO format
                    print(f"📆 Standardized date format in '{col}'")
                else:
                    print(f"⚠️ Skipped date standardization for '{col}' due to insufficient valid dates.")
            except Exception as e:
                print(f"❌ Could not format '{col}': {e}")
        return df

    def standardize_units(self, df: pd.DataFrame):
        """
        Converts different representations of units to a standard unit based on mapping.
        Example: {'kg': ['kilogram', 'kgs', 'kg.', 'kilograms']}
        """
        string_columns = [col for col in df.select_dtypes(include=['object']).columns]

        for col in string_columns:
            for standard_unit, variants in self.unit_map.items():
                df[col] = df[col].str.lower().replace(variants, standard_unit, regex=True)
        
        print("⚖️ Standardized unit representations.")
        return df

    def standardize_boolean_format(self, df: pd.DataFrame):
        """
        Converts yes/no, true/false, y/n, etc., into Python boolean values.
        """
        boolean_columns = [col for col in df.select_dtypes(include=['bool']).columns]

        for col in boolean_columns:
            lowercase_col = df[col].astype(str).str.lower().str.strip()
            df[col] = lowercase_col.map(lambda x: True if x in ['true', 'yes', 'y', '1'] else False)
            print(f"✅ Standardized boolean format in '{col}'")
        
        return df

    def format_all(self, df: pd.DataFrame):
        df = self.standardize_numerical_format(df)
        df = self.standardize_string_format(df)
        df = self.standardize_date_format(df)
        df = self.standardize_units(df)
        df = self.standardize_boolean_format(df)

        # Final adjustment: Convert numeric columns to int if all values have .0, otherwise keep as float
        for col in df.select_dtypes(include=['float']).columns:
            try:
                # Check if all values are integers
                if (df[col].dropna() % 1 == 0).all():
                    df[col] = df[col].astype('Int64')  # Convert to integer type
            except Exception as e:
                print(f"Error adjusting numeric type for column {col}: {e}")

        print("Final numeric type adjustments done ✅")
        print(df.info())
        return df

