# CareFlow Data Cleaning Test Cases

## Objective
Document test cases for validating the event-log cleaning pipeline.

| Test ID | Test Scenario | Expected Result |
|---|---|---|
| TC01 | Missing case ID | Record is excluded from cleaned output. |
| TC02 | Missing activity | Record is excluded from cleaned output. |
| TC03 | Invalid timestamp | Record is excluded from cleaned output. |
| TC04 | Exact duplicate row | Duplicate record is removed. |
| TC05 | Activity label contains extra whitespace | Whitespace is trimmed. |
| TC06 | Valid repeated activity in a case | Valid repeated activity is preserved. |
| TC07 | Events have different timestamps | Events are sorted by case ID and timestamp. |
| TC08 | Medical attributes contain missing values | Missing medical values are preserved. |
| TC09 | Cleaned dataset is validated | Validation script reports PASS when all configured checks succeed. |

## Current Dataset Validation

- Cleaned rows: 15,189
- Unique cases: 1,049
- Unique activities: 16
- Missing case IDs: 0
- Missing activities: 0
- Invalid timestamps: 0
- Exact duplicate rows: 0
- Chronological sorting: Passed

## Execution Note

The table documents expected behavior. These test cases should be executed against controlled sample records before being treated as automated test results.

