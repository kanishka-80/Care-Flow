# CareFlow — Clinical Pathway Process Mining

## 1. Project Overview

CareFlow is a healthcare process analytics project focused on analyzing
hospital event logs to understand patient pathways, activity sequences,
and process behavior.

The project uses the Sepsis Cases - Event Log dataset to prepare
structured event data for data-quality analysis, SQL analytics,
and process mining.

## 2. Dataset Information

- Dataset: Sepsis Cases - Event Log
- Author: Felix Mannhardt
- Institution: Eindhoven University of Technology
- DOI: 10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460
- Approximate size: 1,000 cases and 15,000 events
- Activities: 16

The dataset documentation states that event timestamps have been
randomized while time intervals between events within a trace have
been preserved.

Therefore, timestamps should not be interpreted as actual hospital
calendar dates or times.

Dataset attributes are anonymized according to the supplied dataset
documentation.

## 3. Project Structure

```text
Care-Flow/
├── data/
│   ├── raw/                  # Source dataset files
│   └── processed/            # Converted and cleaned datasets
├── Src/
│   ├── convert_xes.py        # Converts XES event logs to CSV
│   ├── clean_data.py         # Cleans and prepares event data
│   └── validate_data.py      # Validates cleaned data
├── SQL/
│   └── analysis_queries.sql  # SQL analysis queries
├── Reports/
│   └── data_quality_report.md
├── DOCS/                     # Additional documentation
├── Nootbooks/                # Project notebooks
├── requirements.txt          # Python dependencies
└── README.md


4. Prerequisites
Python 3.11
pip
Git
MySQL, if running the SQL analysis queries
5. Installation

Open a terminal in the project directory.

Install the required Python packages:

python -m pip install pandas pm4py
6. Data Processing Workflow
Step 1: Convert XES to CSV

Run:

python Src/convert_xes.py

Input:

data/raw/Sepsis Cases - Event Log (2).xes.gz

Output:

data/processed/sepsis_event_log.csv

Step 2: Clean the Dataset

Run:

python Src/clean_data.py

The cleaning script:

Standardizes column names.
Removes an extra index column when present.
Converts timestamps to UTC-aware datetime values.
Trims whitespace from activity labels.
Removes exact duplicate rows.
Excludes records missing essential event fields.
Sorts events by case ID and timestamp.
Preserves valid repeated activities and medical attributes.

Outputs:

data/processed/cleaned_event_logs.csv
data/processed/excluded_records.csv
Reports/data_quality_report.md
Step 3: Validate the Cleaned Dataset

Run:

python Src/validate_data.py

The validation script checks required columns, missing values,
invalid timestamps, duplicate rows, activity labels, case counts,
and chronological ordering.

7. SQL Analysis

SQL queries are maintained in:

SQL/analysis_queries.sql

The queries cover:

Total events
Unique cases
Unique activities
Events per activity
Events per case
Case duration
Case-level activity diversity

Run the queries using a compatible MySQL database after configuring
the required database and table.

8. Data Quality Results

The previously recorded cleaning run reported:

Original rows: 15,214
Cleaned rows: 15,189
Excluded records: 24
Exact duplicate rows removed: 1
Invalid timestamps: 0
Unique cases after cleaning: 1,049
Unique activities: 16

These results should be updated if the dataset or cleaning process changes.

9. Limitations
Event timestamps have been randomized by the dataset authors.
Absolute timestamps should not be interpreted as actual hospital dates.
Missing medical attributes should not automatically be treated as zero.
Findings should be interpreted in the context of the dataset's documented
limitations.
Dataset timestamps and conversion outputs should be checked before
drawing conclusions from time-based analysis.
10. Team Contributions
Member 1: Data engineering and source event-log preparation.
Member 2: Data cleaning, validation, SQL analysis, and data-quality reporting.
Member 3: Process mining and process discovery.
Member 4: Analytics, dashboard design, and KPI documentation.
11. Reproducibility

Run the conversion, cleaning, and validation scripts in the documented
order. Check their console output and generated files to verify that
the workflow completed successfully.