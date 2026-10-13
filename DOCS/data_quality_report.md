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
