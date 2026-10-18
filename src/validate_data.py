import pandas as pd
from pathlib import Path

# Find the CareFlow project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset location
DATA_FILE = PROJECT_DIR / "data" / "raw" / "hospital_event_logs.csv"

# Required columns
REQUIRED_COLUMNS = [
    "case_id",
    "activity",
    "timestamp",
    "department",
    "doctor_id",
    "outcome"
]


def validate_data():
    # Check whether the dataset exists
    if not DATA_FILE.exists():
        print("FAIL: Dataset file not found!")
        print("Expected location:", DATA_FILE)
        return

    df = pd.read_csv(DATA_FILE)
    errors = []

    print("CareFlow Dataset Validation")
    print("-" * 35)

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
    else:
        print("PASS: All required columns are present.")

        # Check missing and empty values
        for column in REQUIRED_COLUMNS:
            missing_count = df[column].isna().sum()
            empty_count = (
                df[column]
                .astype("string")
                .str.strip()
                .eq("")
                .sum()
            )

            if missing_count or empty_count:
                errors.append(
                    f"{column}: {missing_count} missing, "
                    f"{empty_count} empty values"
                )

        # Validate timestamps
        timestamps = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

        if timestamps.notna().all():
            print("PASS: All timestamps are valid.")
        else:
            errors.append(
                f"Invalid timestamps: {timestamps.isna().sum()}"
            )

        # Check event ordering within each hospital visit
        if timestamps.notna().all() and "case_id" in df.columns:
            check_df = df.assign(_timestamp=timestamps)

            out_of_order = 0
            for _, group in check_df.groupby("case_id"):
                out_of_order += (
                    group["_timestamp"].diff().dropna().lt(
                        pd.Timedelta(0)
                    ).sum()
                )

            if out_of_order == 0:
                print("PASS: Events are chronologically ordered per case.")
            else:
                errors.append(
                    f"Events out of order: {out_of_order}"
                )

    # Display validation results
    if errors:
        print("\nVALIDATION FAILED:")
        for error in errors:
            print("-", error)
    else:
        print("PASS: No missing or empty required values.")
        print("\nVALIDATION SUCCESSFUL!")

    print("-" * 35)
    print("Total event records:", len(df))

    if "case_id" in df.columns:
        print("Total hospital visits:", df["case_id"].nunique())


if __name__ == "__main__":
    validate_data()