# CareFlow Data Quality Report

## Dataset Overview

- Original rows: 15214
- Original columns: 32
- Cleaned rows: 15189
- Cleaned columns: 32
- Unique case IDs: 1049
- Unique activities: 16

## Data Quality Checks

- Missing case IDs before cleaning: 24
- Missing activities before cleaning: 0
- Invalid timestamps: 0
- Exact duplicate rows identified: 1
- Excluded records: 24

## Cleaning Rules

1. Removed the extra Unnamed: 0 index column.
2. Renamed case, activity, and timestamp columns.
3. Converted timestamps to UTC-aware datetime values.
4. Trimmed whitespace from activity labels.
5. Removed exact duplicate records only.
6. Excluded records missing essential event fields.
7. Sorted events by case ID and timestamp.
8. Preserved medical attributes and their missing values.
9. Preserved valid repeated activities.

## Missing Values After Cleaning

InfectionSuspected           14140
org:group                        0
DiagnosticBlood              14140
DisfuncOrg                   14140
SIRSCritTachypnea            14140
Hypotensie                   14140
SIRSCritHeartRate            14140
Infusion                     14140
DiagnosticArtAstrup          14140
activity                         0
Age                          14140
DiagnosticIC                 14140
DiagnosticSputum             14140
DiagnosticLiquor             14140
DiagnosticOther              14140
SIRSCriteria2OrMore          14140
DiagnosticXthorax            14140
SIRSCritTemperature          14140
timestamp                        0
DiagnosticUrinaryCulture     14140
SIRSCritLeucos               14140
Oligurie                     14140
DiagnosticLacticAcid         14140
lifecycle:transition             0
Diagnose                     14394
Hypoxie                      14140
DiagnosticUrinarySediment    14140
DiagnosticECG                14140
case_id                          0
Leucocytes                   11838
CRP                          12071
LacticAcid                   13737

## Output Files

- Cleaned dataset: data/processed/cleaned_event_logs.csv
- Excluded records: data/processed/excluded_records.csv


## SQL Analysis Summary

- Total events: 15,189
- Unique cases: 1,049
- Unique activities: 16
- First recorded event: 2013-11-07 07:18:29 UTC
- Last recorded event: 2015-06-05 10:25:11 UTC

## Analysis Performed

1. Total event count
2. Unique case count
3. Unique activity count
4. Activity-wise event distribution
5. Case-wise event distribution
6. Activity percentage analysis
7. Case duration analysis
8. Cases ranked by event count

## Automated Validation

- Validation script: `Src/validate_data.py`
- Validation report: `Reports/validation_report.txt`
- Latest validation status: PASSED
- Checks include missing IDs, missing activities, invalid timestamps, duplicate rows, unique cases, unique activities, activity whitespace, and chronological sorting.

## Source-to-Target Field Mapping

| Source field | Target field | Transformation |
|---|---|---|
| `case:concept:name` | `case_id` | Renamed; missing IDs excluded |
| `concept:name` | `activity` | Renamed; whitespace trimmed |
| `time:timestamp` | `timestamp` | Renamed; parsed as UTC-aware datetime |
| `lifecycle:transition` | `lifecycle:transition` | Preserved without renaming |
| Other medical attributes | Same field names | Preserved; missing values retained |

The cleaning pipeline removes exact duplicate rows, excludes events missing essential fields, and sorts valid events by case ID and timestamp. Legitimate repeated activities are preserved.

**Output:** `data/processed/cleaned_event_logs.csv`  
**Cleaned rows:** 15,189  
**Unique cases:** 1,049  
**Unique activities:** 16  
**Validation:** Passed using `Src/validate_data.py`

### Large Event Time-Gap Analysis

A SQL query using `LEAD()` and `TIMESTAMPDIFF()` was executed successfully in MySQL 8.0.46 to identify consecutive events separated by more than 24 hours.

The results showed large gaps between some consecutive activities, including `Release A` and `Return ER`. The largest visible gap was 600,855 minutes (approximately 417 days).

These gaps are flagged for further investigation and are not automatically classified as data errors because the dataset uses anonymized timestamps.


### Large Time-Gap Summary

A SQL analysis identified 2,122 consecutive-event gaps exceeding 24 hours. The average gap among these records was 322.98 hours, and the maximum was 100,014.25 hours.

These results require careful interpretation because the dataset uses anonymized timestamps. Large gaps are flagged for investigation and are not automatically classified as data-quality errors.


### Case-Level Large Gap Analysis

A SQL query was used to identify cases with consecutive-event gaps exceeding 24 hours. The top 20 cases were ranked by the number of large gaps.

Case NGA had 24 large gaps, with a maximum gap of 170 hours. These results are flagged for investigation and are not automatically classified as data-quality errors because the dataset uses anonymized timestamps.


## Activity Transition Analysis

### Objective

The objective of this analysis is to identify frequently occurring consecutive activity patterns in the hospital event log.

### Methodology

SQL window functions were used to identify the next activity within each patient case.

* `LEAD()` was used to retrieve the next activity.
* `PARTITION BY case_id` ensured that activities were analysed separately for each case.
* `ORDER BY timestamp` maintained chronological event order.
* `GROUP BY` was used to calculate transition frequencies.

### Observed Results

| Current Activity | Next Activity    | Transition Count |
| ---------------- | ---------------- | ---------------: |
| Leucocytes       | CRP              |             1774 |
| CRP              | Leucocytes       |             1443 |
| ER Registration  | ER Triage        |              970 |
| ER Triage        | ER Sepsis Triage |              904 |
| CRP              | LacticAcid       |              627 |

### Conclusion

The analysis identified frequently occurring activity transitions in the hospital event log. These patterns help us understand the sequence of recorded hospital activities and support further process analysis.


## Activity Transition Percentage Analysis

### Objective

The objective of this analysis is to calculate the percentage contribution of each consecutive activity transition in the hospital event log.

### Methodology

SQL Common Table Expressions (CTEs) and window functions were used to calculate activity transition frequencies and percentages.

* LEAD() identifies the next activity within each case.
* PARTITION BY case_id separates individual patient cases.
* GROUP BY calculates transition frequencies.
* SUM() OVER() calculates the total number of transitions.
* ROUND() formats percentages to two decimal places.

### Key Findings

| Activity Transition          | Count | Percentage |
| ---------------------------- | ----: | ---------: |
| Leucocytes → CRP             |  1774 |     12.55% |
| CRP → Leucocytes             |  1443 |     10.21% |
| ER Registration → ER Triage  |   970 |      6.86% |
| ER Triage → ER Sepsis Triage |   904 |      6.39% |
| CRP → LacticAcid             |   627 |      4.43% |

### Conclusion

The analysis identified frequently occurring activity transitions and calculated their percentage contribution to all consecutive transitions. These findings provide insights into common activity sequences in the hospital event log.



## Case HG Time-Gap Investigation

### Objective

To investigate the unusually long recorded duration of Case HG by calculating the time differences between consecutive activities.

### Methodology

The SQL LEAD() window function was used to retrieve the next activity and its timestamp within the same case.

TIMESTAMPDIFF() was used to calculate the time difference in hours and days.

### Key Findings

* Case ID: HG
* Total recorded duration: 422.32 days
* First recorded event: ER Registration
* Last recorded event: Return ER
* Largest consecutive event gap: 417.26 days
* Gap occurred between Release A and Return ER.

### Conclusion

The investigation identified a significant time gap of 417.26 days between Release A and Return ER. This gap accounts for most of the total recorded case duration.

This finding represents a difference between recorded event timestamps and does not establish continuous hospital admission.
