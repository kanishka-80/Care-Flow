USE careflow;

-- 1. Total events
SELECT COUNT(*) AS total_events
FROM cleaned_event_logs;

-- 2. Total unique cases
SELECT COUNT(DISTINCT case_id) AS total_cases
FROM cleaned_event_logs;

-- 3. Total unique activities
SELECT COUNT(DISTINCT activity) AS total_activities
FROM cleaned_event_logs;

-- 4. Event count by activity
SELECT
    activity,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY activity
ORDER BY event_count DESC;

-- 5. Percentage of events by activity
SELECT
    activity,
    COUNT(*) AS total_events,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM cleaned_event_logs),
        2
    ) AS event_percentage
FROM cleaned_event_logs
GROUP BY activity
ORDER BY total_events DESC;

-- 6. Event count by case
SELECT
    case_id,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY event_count DESC;

-- 7. Case duration in hours
SELECT
    case_id,
    MIN(timestamp) AS first_event_time,
    MAX(timestamp) AS last_event_time,
    TIMESTAMPDIFF(
        HOUR,
        MIN(timestamp),
        MAX(timestamp)
    ) AS recorded_duration_hours
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY recorded_duration_hours DESC;

-- 8. Combined case summary
SELECT
    case_id,
    COUNT(*) AS total_events,
    MIN(timestamp) AS first_event_time,
    MAX(timestamp) AS last_event_time,
    TIMESTAMPDIFF(
        HOUR,
        MIN(timestamp),
        MAX(timestamp)
    ) AS recorded_duration_hours
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY total_events DESC;

-- 9. Case activity diversity
-- Count distinct activities performed in each case

SELECT
    case_id,
    COUNT(*) AS total_events,
    COUNT(DISTINCT activity) AS unique_activities
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY unique_activities DESC, total_events DESC;


-- 10. Data Quality Validation Checks

-- A. Check missing case IDs
SELECT COUNT(*) AS missing_case_ids
FROM cleaned_event_logs
WHERE case_id IS NULL;

-- B. Check missing activity names
SELECT COUNT(*) AS missing_activities
FROM cleaned_event_logs
WHERE activity IS NULL
   OR TRIM(activity) = '';

-- C. Check invalid timestamps
SELECT COUNT(*) AS invalid_timestamps
FROM cleaned_event_logs
WHERE timestamp IS NULL;

-- D. Check exact duplicate event records
SELECT
    case_id,
    activity,
    timestamp,
    COUNT(*) AS duplicate_count
FROM cleaned_event_logs
GROUP BY case_id, activity, timestamp
HAVING COUNT(*) > 1;

-- E. Check events with identical timestamps within a case
SELECT
    case_id,
    timestamp,
    COUNT(*) AS events_at_same_timestamp
FROM cleaned_event_logs
GROUP BY case_id, timestamp
HAVING COUNT(*) > 1;

-- F. Check activity labels with leading or trailing spaces
SELECT COUNT(*) AS activity_labels_with_extra_spaces
FROM cleaned_event_logs
WHERE activity <> TRIM(activity);