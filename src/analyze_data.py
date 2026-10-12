import pandas as pd
from pathlib import Path

# Find the CareFlow project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load hospital event data
file_path = BASE_DIR / "data" / "raw" / "Hospital_event_logs.csv"
df = pd.read_csv(file_path)

# Display basic information
print("CARE FLOW - HOSPITAL DATA ANALYSIS")
print("=" * 40)

print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nAnalysis completed successfully!")