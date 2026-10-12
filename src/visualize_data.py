import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load cleaned hospital data
file_path = BASE_DIR / "data" / "processed" / "Hospital_event_logs_cleaned.csv"
df = pd.read_csv(file_path)

print("CARE FLOW - HOSPITAL ACTIVITY ANALYSIS")
print("=" * 40)

# Count hospital events by activity
activity_counts = df["activity"].value_counts().head(10)

print("\nHospital events by activity:")
print(activity_counts)

# Create bar chart
plt.figure(figsize=(10, 6))
activity_counts.plot(kind="bar")

plt.title("Top 10 Hospital Activities")
plt.xlabel("Hospital Activity")
plt.ylabel("Number of Records")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save chart
output_dir = BASE_DIR / "reports" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "hospital_activity_chart.png"
plt.savefig(output_file, dpi=150)

print("\nChart saved successfully!")
print("Saved at:", output_file)

plt.show()