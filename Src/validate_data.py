import pandas as pd
from pathlib import Path

# ==========================================
# CAREFLOW - DATA QUALITY VALIDATION
# Member 2: Data Cleaning & SQL
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_event_logs.csv"
)

REQUIRED_COLUMNS = ["case_id", "activity", "timestamp"]


def validate_data():
    print("=" * 50)
    print("CAREFLOW - DATA QUALITY VALIDATION")
    print("=" * 50)

    # Check whether input file exists
    if not INPUT_FILE.exists():
        print(f"ERROR: Dataset not found: {INPUT_FILE}")
        return False

    # Load dataset
    df = pd.read_csv(INPUT_FILE)

    print(f"\nDataset loaded: {INPUT_FILE.name}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        print(f"\nFAILED: Missing columns: {missing_columns}")
        return False

    # Validation checks
    checks = {}

    checks["Missing case IDs"] = df["case_id"].isna().sum()
    checks["Missing activities"] = df["activity"].isna().sum()

    # Parse timestamps without modifying the original dataset
    timestamps = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True
    )

    checks["Invalid timestamps"] = timestamps.isna().sum()
    checks["Exact duplicate rows"] = df.duplicated().sum()

    checks["Unique cases"] = df["case_id"].nunique()
    checks["Unique activities"] = df["activity"].nunique()

    checks["Activity labels with extra spaces"] = (
        df["activity"].astype(str)
        != df["activity"].astype(str).str.strip()
    ).sum()

    # Check chronological ordering within cases
    sorted_df = df.assign(timestamp=timestamps).sort_values(
        ["case_id", "timestamp"]
    ).reset_index(drop=True)

    current_df = df.assign(timestamp=timestamps).reset_index(drop=True)

    checks["Rows correctly sorted"] = (
        current_df.equals(sorted_df)
    )

    # Display results
    print("\nVALIDATION RESULTS")
    print("-" * 50)

    for check, result in checks.items():
        print(f"{check}: {result}")

    # Required data-quality rules
    failures = []

    for check in [
        "Missing case IDs",
        "Missing activities",
        "Invalid timestamps",
        "Exact duplicate rows",
        "Activity labels with extra spaces",
    ]:
        if checks[check] != 0:
            failures.append(check)

    if not checks["Rows correctly sorted"]:
        failures.append("Rows correctly sorted")

    print("\n" + "=" * 50)

    if failures:
        print("VALIDATION STATUS: FAILED")
        print("Issues found:")

        for failure in failures:
            print(f"- {failure}")

        return False

    print("VALIDATION STATUS: PASSED")
    print("All configured data-quality checks passed.")

    return True


if __name__ == "__main__":
    success = validate_data()

    if not success:
        raise SystemExit(1)