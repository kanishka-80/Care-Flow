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

-- 11. Consecutive activity sequence and time gaps
WITH ordered_events AS (
    SELECT
        case_id,
        activity,
        timestamp,
        LEAD(activity) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_activity,
        LEAD(timestamp) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_timestamp
    FROM cleaned_event_logs
)
SELECT
    case_id,
    activity AS current_activity,
    next_activity,
    timestamp AS current_timestamp,
    next_timestamp,
    TIMESTAMPDIFF(
        MINUTE,
        timestamp,
        next_timestamp
    ) AS gap_minutes
FROM ordered_events
WHERE next_activity IS NOT NULL
ORDER BY case_id, timestamp;

SELECT
    case_id,
    activity,
    next_activity,
    gap_minutes
FROM (
    SELECT
        case_id,
        activity,
        LEAD(activity) OVER (
            PARTITION BY case_id ORDER BY `timestamp`
        ) AS next_activity,
        TIMESTAMPDIFF(
            MINUTE,
            `timestamp`,
            LEAD(`timestamp`) OVER (
                PARTITION BY case_id ORDER BY `timestamp`
            )
        ) AS gap_minutes
    FROM cleaned_event_logs
) AS gaps
WHERE gap_minutes > 1440
ORDER BY gap_minutes DESC;


SELECT
    COUNT(*) AS total_large_gaps,
    ROUND(AVG(gap_minutes) / 60, 2) AS avg_gap_hours,
    ROUND(MAX(gap_minutes) / 60, 2) AS max_gap_hours
FROM (
    SELECT TIMESTAMPDIFF(
        MINUTE,
        `timestamp`,
        LEAD(`timestamp`) OVER (
            PARTITION BY case_id ORDER BY `timestamp`
        )
    ) AS gap_minutes
    FROM cleaned_event_logs
) AS gaps
WHERE gap_minutes > 1440;

SELECT
    case_id,
    COUNT(*) AS large_gap_count,
    ROUND(MAX(gap_minutes) / 60, 2) AS max_gap_hours
FROM (
    SELECT
        case_id,
        TIMESTAMPDIFF(
            MINUTE,
            `timestamp`,
            LEAD(`timestamp`) OVER (
                PARTITION BY case_id
                ORDER BY `timestamp`
            )
        ) AS gap_minutes
    FROM cleaned_event_logs
) AS gaps
WHERE gap_minutes > 1440
GROUP BY case_id
ORDER BY large_gap_count DESC
LIMIT 20;

-- 15. Activity Transition Frequency

WITH activity_transitions AS (
    SELECT
        activity AS current_activity,
        LEAD(activity) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_activity
    FROM cleaned_event_logs
)

SELECT
    current_activity,
    next_activity,
    COUNT(*) AS transition_count
FROM activity_transitions
WHERE next_activity IS NOT NULL
GROUP BY current_activity, next_activity
ORDER BY transition_count DESC;

-- 16. Activity Transition Percentage Analysis

WITH activity_transitions AS (
    SELECT
        activity AS current_activity,

        LEAD(activity) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_activity

    FROM cleaned_event_logs
),

transition_counts AS (
    SELECT
        current_activity,
        next_activity,
        COUNT(*) AS transition_count

    FROM activity_transitions

    WHERE next_activity IS NOT NULL

    GROUP BY current_activity, next_activity
)

SELECT
    current_activity,
    next_activity,
    transition_count,

    ROUND(
        transition_count * 100.0 /
        SUM(transition_count) OVER (),
        2
    ) AS transition_percentage

FROM transition_counts

ORDER BY transition_count DESC;

-- 17. Patient Case Duration Summary

WITH case_durations AS (
    SELECT
        case_id,

        MIN(timestamp) AS first_event_time,

        MAX(timestamp) AS last_event_time,

        TIMESTAMPDIFF(
            MINUTE,
            MIN(timestamp),
            MAX(timestamp)
        ) AS duration_minutes

    FROM cleaned_event_logs

    GROUP BY case_id
)

SELECT
    COUNT(*) AS total_cases,

    ROUND(AVG(duration_minutes) / 60, 2)
        AS average_duration_hours,

    ROUND(MIN(duration_minutes) / 60, 2)
        AS minimum_duration_hours,

    ROUND(MAX(duration_minutes) / 60, 2)
        AS maximum_duration_hours

FROM case_durations;

-- 18. Top 10 Longest Recorded Case Durations

SELECT
    case_id,

    MIN(timestamp) AS first_event_time,

    MAX(timestamp) AS last_event_time,

    ROUND(
        TIMESTAMPDIFF(
            MINUTE,
            MIN(timestamp),
            MAX(timestamp)
        ) / 60,
        2
    ) AS duration_hours,

    ROUND(
        TIMESTAMPDIFF(
            MINUTE,
            MIN(timestamp),
            MAX(timestamp)
        ) / 1440,
        2
    ) AS duration_days

FROM cleaned_event_logs

GROUP BY case_id

ORDER BY duration_hours DESC

LIMIT 10;

-- 19. Detailed Investigation of Longest Duration Case

SELECT
    case_id,
    activity,
    timestamp,

    ROW_NUMBER() OVER (
        PARTITION BY case_id
        ORDER BY timestamp
    ) AS event_sequence

FROM cleaned_event_logs

WHERE case_id = 'HG'

ORDER BY timestamp;

-- 20. Event Time Gap Investigation for Case HG

WITH ordered_events AS (

    SELECT
        case_id,
        activity,
        timestamp,

        LEAD(activity) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_activity,

        LEAD(timestamp) OVER (
            PARTITION BY case_id
            ORDER BY timestamp
        ) AS next_timestamp

    FROM cleaned_event_logs

    WHERE case_id = 'HG'
)

SELECT
    case_id,

    activity AS current_activity,

    next_activity,

    timestamp AS current_event_time,

    next_timestamp,

    ROUND(
        TIMESTAMPDIFF(
            MINUTE,
            timestamp,
            next_timestamp
        ) / 60,
        2
    ) AS gap_hours,

    ROUND(
        TIMESTAMPDIFF(
            MINUTE,
            timestamp,
            next_timestamp
        ) / 1440,
        2
    ) AS gap_days

FROM ordered_events

WHERE next_timestamp IS NOT NULL

ORDER BY timestamp;