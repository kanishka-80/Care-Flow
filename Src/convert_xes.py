import pm4py
import pandas as pd
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output file paths
input_file = PROJECT_ROOT / "data" / "RAW" / "Sepsis Cases - Event Log (2).xes.gz"
output_file = PROJECT_ROOT / "data" / "processed" / "sepsis_event_log.csv"

# Check whether the dataset exists
if not input_file.exists():
    print("Dataset file not found!")
    print("Expected location:", input_file)

else:
    print("Loading XES dataset...")

    # Read XES file
    log = pm4py.read_xes(str(input_file))

    # Convert event log into DataFrame
    df = pm4py.convert_to_dataframe(log)

    # Display basic information
    print("\nDataset loaded successfully!")
    print("Shape:", df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst five rows:")
    print(df.head())

    # Create processed folder if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Export to CSV
    df.to_csv(output_file, index=False)

    print("\nCSV saved successfully!")
    print("Output location:", output_file)