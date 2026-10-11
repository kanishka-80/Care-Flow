import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output paths
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

REPORT_FILE = (
    PROJECT_ROOT
    / "Reports"
    / "data_quality_report.md"
)

# 1. Load original converted dataset
df = pd.read_csv(INPUT_FILE)

raw_rows = len(df)

# 2. Record initial data quality
missing_before = df.isnull().sum()

# 3. Standardize column names
df = df.rename(columns={
    "case:concept:name": "case_id",
    "concept:name": "activity",
    "time:timestamp": "timestamp"
})

# 4. Convert timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

# 5. Identify invalid records
missing_case_ids = int(df["case_id"].isna().sum())
missing_activities = int(df["activity"].isna().sum())
invalid_timestamps = int(df["timestamp"].isna().sum())

# 6. Standardize activity labels
df["activity"] = df["activity"].replace({
    "Xray": "X-Ray",
    "X-Ray": "X-Ray"
})

# 7. Identify exact duplicate rows
duplicate_count = int(df.duplicated().sum())

# Remove exact duplicates only
df = df.drop_duplicates()

# 8. Remove records missing essential event fields
# Keep a copy of excluded rows for investigation
invalid_mask = (
    df["case_id"].isna()
    | df["activity"].isna()
    | df["timestamp"].isna()
)

invalid_records = df[invalid_mask].copy()

df = df[~invalid_mask].copy()

# 9. Sort events
df = df.sort_values(
    ["case_id", "timestamp"],
    kind="stable"
).reset_index(drop=True)

# 10. Save cleaned dataset
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

# 11. Save excluded records for review
INVALID_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "excluded_invalid_records.csv"
)

invalid_records.to_csv(INVALID_FILE, index=False)

# 12. Generate quality report
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

missing_after = df.isnull().sum()

report = f"""# CareFlow Data Quality Report

## Dataset Overview

- Input file: sepsis_event_log.csv
- Initial rows: {raw_rows}
- Initial columns: {len(pd.read_csv(INPUT_FILE, nrows=0).columns)}
- Final cleaned rows: {len(df)}
- Final columns: {len(df.columns)}

## Data Quality Checks

- Missing case IDs before cleaning: {missing_case_ids}
- Missing activity names before cleaning: {missing_activities}
- Invalid timestamps before cleaning: {invalid_timestamps}
- Exact duplicate rows identified: {duplicate_count}
- Records excluded for missing essential fields: {len(invalid_records)}

## Cleaning Rules

1. Renamed case ID, activity, and timestamp columns.
2. Converted timestamps to UTC-aware datetime values.
3. Standardized selected activity labels.
4. Removed exact duplicate rows.
5. Excluded records missing essential event fields.
6. Sorted events by case ID and timestamp.
7. Preserved medical attributes and their missing values.
8. Preserved valid repeated activities.

## Output Files

- Cleaned dataset: data/processed/cleaned_event_logs.csv
- Excluded records: data/processed/excluded_invalid_records.csv

## Missing Values After Cleaning

{missing_after.to_string()}
"""

REPORT_FILE.write_text(report, encoding="utf-8")

# 13. Display summary
print("=" * 50)
print("CAREFLOW DATA CLEANING COMPLETED")
print("=" * 50)

print("Original rows:", raw_rows)
print("Final cleaned rows:", len(df))
print("Duplicate rows removed:", duplicate_count)
print("Excluded invalid records:", len(invalid_records))
print("Invalid timestamps found:", invalid_timestamps)

print("\nCleaned dataset saved at:")
print(OUTPUT_FILE)

print("\nQuality report saved at:")
print(REPORT_FILE)

print("\nExcluded records saved at:")
print(INVALID_FILE)