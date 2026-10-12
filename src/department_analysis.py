import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate CareFlow project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load cleaned hospital data
file_path = BASE_DIR / "data" / "processed" / "Hospital_event_logs_cleaned.csv"
df = pd.read_csv(file_path)

print("CARE FLOW - DEPARTMENT ANALYSIS")
print("=" * 40)

# Count records for each department
department_counts = df["department"].value_counts()

print("\nRecords by Department:")
print(department_counts)

# Create department-wise chart
plt.figure(figsize=(10, 6))
department_counts.plot(kind="bar")

plt.title("Hospital Events by Department")
plt.xlabel("Department")
plt.ylabel("Number of Records")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save chart
output_dir = BASE_DIR / "reports" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "department_analysis_chart.png"
plt.savefig(output_file, dpi=150)

print("\nDepartment chart saved successfully!")
print("Saved at:", output_file)

plt.show()