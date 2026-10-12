import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

# Keep the generated data reproducible
random.seed(42)

# Find the CareFlow project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Create the folder for raw data
OUTPUT_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Activities in a fictional hospital visit
activities = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "Laboratory Test",
    "X-Ray",
    "Pharmacy",
    "Discharge"
]

departments = [
    "Emergency",
    "General Medicine",
    "Orthopaedics"
]

events = []

# Generate 100 fictional hospital visits
for visit_number in range(1, 101):

    case_id = f"CASE{visit_number:03d}"

    # Every visit begins with registration, triage and consultation
    sequence = [
        "Registration",
        "Triage",
        "Doctor Consultation"
    ]

    # Some visits include additional tests
    if random.random() < 0.65:
        sequence.append("Laboratory Test")

    if random.random() < 0.30:
        sequence.append("X-Ray")

    sequence.extend(["Pharmacy", "Discharge"])

    # Simulate repeated triage in some visits
    if visit_number % 10 == 0:
        sequence.insert(2, "Triage")

    # Set a starting date and time
    current_time = datetime(2026, 10, 1, 8, 0, 0)
    current_time += timedelta(minutes=random.randint(0, 600))

    for activity in sequence:

        # Normal time between activities
        gap_minutes = random.randint(5, 45)

        # Simulate a long delay for selected visits
        if (
            visit_number % 15 == 0
            and activity == "Laboratory Test"
        ):
            gap_minutes = 240

        current_time += timedelta(minutes=gap_minutes)

        events.append({
            "case_id": case_id,
            "activity": activity,
            "timestamp": current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "department": random.choice(departments),
            "doctor_id": f"DOC{random.randint(1, 10):03d}",
            "outcome": "Discharged"
        })

# Convert the records into a table
df = pd.DataFrame(events)

# Save the CSV file
output_file = OUTPUT_DIR / "hospital_event_logs.csv"
df.to_csv(output_file, index=False)

print("CareFlow synthetic dataset created!")
print("Total event records:", len(df))
print("Total hospital visits:", df["case_id"].nunique())
print("Saved file:", output_file)
print("\nFirst 5 records:")
print(df.head())s