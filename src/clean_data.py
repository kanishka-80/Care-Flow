import pandas as pd
from pathlib import Path

# Locate the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Read the raw hospital data
input_file = BASE_DIR / "data" / "raw" / "Hospital_event_logs.csv"
df = pd.read_csv(input_file)

print("CARE FLOW - DATA CLEANING")
print("=" * 35)

print("Original rows:", len(df))

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing values in text columns
for column in df.select_dtypes(include=["object"]).columns:
    df[column] = df[column].fillna("Unknown")

# Handle missing values in numeric columns
for column in df.select_dtypes(include=["number"]).columns:
    df[column] = df[column].fillna(df[column].median())

print("Rows after removing duplicates:", len(df))
print("Remaining missing values:", df.isnull().sum().sum())

# Save cleaned data
output_dir = BASE_DIR / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "Hospital_event_logs_cleaned.csv"
df.to_csv(output_file, index=False)

print("\nCleaned data saved successfully!")
print("File:", output_file)