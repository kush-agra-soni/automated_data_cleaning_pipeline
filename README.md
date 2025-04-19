# Automated Data Cleaning Pipeline

This project is a **modular, production-ready automatic data cleaning pipeline** built in Python. It standardizes, cleans, and prepares messy real-world datasets for machine learning and analytics workflows.

The pipeline is designed with **two modes of data ingestion**:

---

### 1. Manual Data Injection
Users can upload CSV, JSON, or XLSX files via a local interface. The pipeline runs all cleaning modules sequentially to produce a fully cleaned, ready-to-model DataFrame.

---

### 2. Scheduled Data Injection (PostgreSQL + Cron + CI/CD)
- The pipeline can be connected to a PostgreSQL database using credentials (host, port, database, user, password).
- A cron job is configured to trigger the ingestion automatically at a user-defined interval (e.g., daily at midnight).
- GitHub Actions are integrated to support CI/CD, allowing auto-pull, build, and run on any config update.
- The ingestion process extracts raw data from the database, sends it through the cleaning pipeline, and stores the output (locally or to cloud storage).

---

## Pipeline Architecture
The data cleaning logic is broken into modular files to ensure proper execution order and separation of concerns.

Each module contains specific transformation logic, and together they form the complete cleaning pipeline:

---

### Step-by-Step Execution Order

#### 1. **Column Name Cleaning & Structural Cleanup**
- `remove_special_characters`
- `convert_to_lowercase`
- `remove_whitespace`
- `replace_space_with_underscore`
- `remove_empty_columns`
- `remove_empty_rows`
- `remove_duplicates`

#### 2. **Formatting & Standardization**
- `standardize_numerical_format`
- `standardize_string_format`
- `standardize_date_format`
- `standardize_units`
- `standardize_boolean_format`

#### 3. **Identifier & Redundant Columns**
- `identifier_column_remover`

#### 4. **Type Detection & Correction**
- `detect_types_proactively`
- `convert_types_as_needed`
- `enforce_column_types`

#### 5. **Outlier Detection + Removal**
- `fit_outlier_bounds`
- `remove_outliers`
- `detect_and_remove_outliers`
- `visualize_outliers` *(Optional)*

#### 6. **Missing Value Imputation**
- `drop_high_nan_rows`
- `impute_missing_values`

#### 7. **Date/Time Feature Engineering**
- `extract_dates`

#### 8. **Boolean Normalization (Final Pass)**
- `normalize_booleans`

#### 9. **Encoding (Categoricals to Numbers)**
- `fit_label_encoders`
- `transform_label_encoders`
- `fit_onehot_encoders`
- `transform_onehot_encoders`
- `fit_ordinal_encoders`
- `transform_ordinal_encoders`
- `frequency_encoder`
- `encode_all`

#### 10. **Imbalance Handling (For Classification)**
- `fit_resampler`
- `apply_resampling`
- `visualize_class_distribution` *(Optional)*

#### 11. **Feature Selection & Importance**
- `fit_feature_selector`
- `drop_selected_features`
- `auto_feature_importance`

#### 12. **Feature Scaling**
- `fit_scaler`
- `transform_scaler`
- `visualize_scaling_effect` *(Optional)*

#### 13. **Final Validation & QA**
- `check_final_nans`
- `check_invalid_types`
- `recheck_outliers`
- `visualize_data_distribution` *(Optional)*

---

## Tech Stack
- Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Dateutil, etc.)
- PostgreSQL (Scheduled DB ingestion)
- Cron Jobs (automated scheduling)
- GitHub Actions (CI/CD automation)

---

## Purpose
This project is meant for real-world messy datasets and is adaptable to pipelines for:
- Machine Learning
- Business Intelligence
- ETL Systems
- SaaS Data Products

---
