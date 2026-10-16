import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load events per patient case
file_path = "data/processed/events_per_case.csv"
df = pd.read_csv(file_path)

# Create reports folder
output_folder = Path("reports")
output_folder.mkdir(parents=True, exist_ok=True)

# Events per patient case distribution
plt.figure(figsize=(10, 6))
plt.hist(df["event_count"], bins=20, edgecolor="black")

plt.xlabel("Number of Events per Patient Case")
plt.ylabel("Number of Patient Cases")
plt.title("Distribution of Events per Sepsis Patient Case")

plt.tight_layout()
plt.savefig(output_folder / "sepsis_events_per_case.png")
plt.show()

print("Chart saved: reports/sepsis_events_per_case.png")
print("Patient case visualization completed!")