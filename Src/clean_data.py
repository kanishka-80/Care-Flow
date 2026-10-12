import pandas as pd
from pathlib import Path

# ==========================================
# CAREFLOW - DATA CLEANING
# Member 2: Data Cleaning & SQL
# ==========================================

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# File paths
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sepsis_event_log.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_event_logs.csv"
)

EXCLUDED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "excluded_records.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "Reports"
    / "data_quality_report.md"
)

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(INPUT_FILE)

initial_rows = len(df)

print("=" * 50)
print("CAREFLOW DATA CLEANING STARTED")
print("=" * 50)

print("\nOriginal dataset shape:", df.shape)

# ==========================================
# 2. REMOVE EXTRA INDEX COLUMN
# ==========================================

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])
    print("\nRemoved extra index column: Unnamed: 0")

# ==========================================
# 3. STANDARDIZE COLUMN NAMES
# ==========================================

df = df.rename(columns={
    "case:concept:name": "case_id",
    "concept:name": "activity",
    "time:timestamp": "timestamp"
})

# ==========================================
# 4. CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "case_id",
    "activity",
    "timestamp"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )

# ==========================================
# 5. VALIDATE TIMESTAMPS
# ==========================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

invalid_timestamps = int(
    df["timestamp"].isna().sum()
)

missing_case_ids = int(
    df["case_id"].isna().sum()
)

missing_activities = int(
    df["activity"].isna().sum()
)

print("\nMissing case IDs:", missing_case_ids)
print("Missing activities:", missing_activities)
print("Invalid timestamps:", invalid_timestamps)

# ==========================================
# 6. STANDARDIZE ACTIVITY LABELS
# ==========================================

# Preserve original labels unless a verified
# standardization rule is available.

df["activity"] = df["activity"].astype("string").str.strip()

# ==========================================
# 7. IDENTIFY EXACT DUPLICATES
# ==========================================

duplicate_count = int(df.duplicated().sum())

print("\nExact duplicate rows:", duplicate_count)

# Remove exact duplicates only.
# Repeated activities are preserved.

df = df.drop_duplicates().copy()

# ==========================================
# 8. SEPARATE INVALID EVENT RECORDS
# ==========================================

invalid_mask = (
    df["case_id"].isna()
    | df["activity"].isna()
    | df["timestamp"].isna()
)

excluded_records = df.loc[invalid_mask].copy()

cleaned_df = df.loc[~invalid_mask].copy()

print(
    "Records excluded due to missing essential fields:",
    len(excluded_records)
)

# ==========================================
# 9. SORT EVENTS
# ==========================================

cleaned_df = cleaned_df.sort_values(
    ["case_id", "timestamp"],
    kind="stable"
).reset_index(drop=True)

# ==========================================
# 10. SAVE OUTPUT FILES
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

cleaned_df.to_csv(
    OUTPUT_FILE,
    index=False
)

excluded_records.to_csv(
    EXCLUDED_FILE,
    index=False
)

# ==========================================
# 11. GENERATE DATA QUALITY REPORT
# ==========================================

missing_values = cleaned_df.isna().sum()

report = f"""# CareFlow Data Quality Report

## Dataset Overview

- Original rows: {initial_rows}
- Original columns: {initial_rows and len(pd.read_csv(INPUT_FILE, nrows=0).columns)}
- Cleaned rows: {len(cleaned_df)}
- Cleaned columns: {len(cleaned_df.columns)}
- Unique case IDs: {cleaned_df['case_id'].nunique()}
- Unique activities: {cleaned_df['activity'].nunique()}

## Data Quality Checks

- Missing case IDs before cleaning: {missing_case_ids}
- Missing activities before cleaning: {missing_activities}
- Invalid timestamps: {invalid_timestamps}
- Exact duplicate rows identified: {duplicate_count}
- Excluded records: {len(excluded_records)}

## Cleaning Rules

1. Removed the extra Unnamed: 0 index column.
2. Renamed case, activity, and timestamp columns.
3. Converted timestamps to UTC-aware datetime values.
4. Trimmed whitespace from activity labels.
5. Removed exact duplicate records only.
6. Excluded records missing essential event fields.
7. Sorted events by case ID and timestamp.
8. Preserved medical attributes and their missing values.
9. Preserved valid repeated activities.

## Missing Values After Cleaning

{missing_values.to_string()}

## Output Files

- Cleaned dataset: data/processed/cleaned_event_logs.csv
- Excluded records: data/processed/excluded_records.csv
"""

REPORT_FILE.write_text(
    report,
    encoding="utf-8"
)

# ==========================================
# 12. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 50)
print("DATA CLEANING COMPLETED")
print("=" * 50)

print("Original rows:", initial_rows)
print("Cleaned rows:", len(cleaned_df))
print("Excluded records:", len(excluded_records))
print("Exact duplicates removed:", duplicate_count)

print("\nCleaned dataset:")
print(OUTPUT_FILE)

print("\nExcluded records:")
print(EXCLUDED_FILE)

print("\nData quality report:")
print(REPORT_FILE)