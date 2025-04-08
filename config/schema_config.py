# config/schema_config.py

NUMERICAL_COLUMNS = [
    "Social_media_followers",
    # Add more numerical columns here
]

CATEGORICAL_COLUMNS = [
    "Genre",
    # Add more categorical columns here
]

TARGET_COLUMN = "Sold_out"  # Update if your target changes

# Threshold to drop rows with too many missing values
ROW_DROP_NAN_THRESHOLD = 0.75

# Imputation strategies
IMPUTATION_STRATEGY = {
    "numerical": "mean",
    "categorical": "most_frequent"
}

# Scaling options (can be expanded to minmax, robust, etc.)
SCALING_STRATEGY = "standard"  # Only 'standard' is supported for now

# Encoding options
ENCODING_STRATEGY = "onehot"  # Can extend to ordinal or label encoding
