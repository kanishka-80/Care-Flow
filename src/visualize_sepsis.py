import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load analysis results
file_path = "data/processed/activity_frequency.csv"
df = pd.read_csv(file_path)

# Create output folder for charts
output_folder = Path("reports")
output_folder.mkdir(parents=True, exist_ok=True)

# Chart 1: Top 10 hospital activities
top_activities = df.sort_values(
    "event_count", ascending=False
).head(10)

plt.figure(figsize=(10, 6))
plt.barh(
    top_activities["activity"][::-1],
    top_activities["event_count"][::-1]
)
plt.xlabel("Number of Events")
plt.ylabel("Hospital Activity")
plt.title("Top 10 Activities in Sepsis Patient Data")
plt.tight_layout()
plt.savefig(output_folder / "sepsis_top_activities.png")
plt.show()

print("Chart saved: reports/sepsis_top_activities.png")
print("Sepsis visualization completed!")