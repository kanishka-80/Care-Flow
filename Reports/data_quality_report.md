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