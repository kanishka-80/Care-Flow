import pandas as pd
from pathlib import Path

# Load cleaned dataset
file_path = "data/processed/sepsis_event_log_cleaned.csv"
df = pd.read_csv(file_path)

# Convert timestamp
df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce", utc=True
)

# 1. Activity frequency
activity_counts = df["activity"].value_counts()

print("\n1. Activity Frequency:")
print(activity_counts.to_string())

# 2. Events per patient case
events_per_case = df.groupby("case_id").size()

print("\n2. Events per Patient Case:")
print(events_per_case.describe())

# 3. Most common activities for each case sequence
case_sequences = (
    df.sort_values(["case_id", "timestamp"])
    .groupby("case_id")["activity"]
    .apply(lambda activities: " -> ".join(activities))
)

print("\n3. Sample Patient Journeys:")
for case_id, sequence in case_sequences.head(5).items():
    print(f"\nCase {case_id}: {sequence}")

# 4. Save analysis results
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

activity_counts.rename_axis("activity").reset_index(
    name="event_count"
).to_csv(output_folder / "activity_frequency.csv", index=False)

events_per_case.rename_axis("case_id").reset_index(
    name="event_count"
).to_csv(output_folder / "events_per_case.csv", index=False)

case_sequences.rename_axis("case_id").reset_index(
    name="activity_sequence"
).to_csv(output_folder / "patient_journeys.csv", index=False)

print("\nAnalysis completed!")
print("Saved activity_frequency.csv")
print("Saved events_per_case.csv")
print("Saved patient_journeys.csv")