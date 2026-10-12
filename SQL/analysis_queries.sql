-- 1. Total events
SELECT COUNT(*) AS total_events
FROM cleaned_event_logs;

-- 2. Total unique cases
SELECT COUNT(DISTINCT case_id) AS total_cases
FROM cleaned_event_logs;

-- 3. Unique activities
SELECT COUNT(DISTINCT activity) AS total_activities
FROM cleaned_event_logs;

-- 4. Events per activity
SELECT
    activity,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY activity
ORDER BY event_count DESC;

-- 5. Events per case
SELECT
    case_id,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY event_count DESC;

USE careflow;

SELECT COUNT(DISTINCT case_id) AS total_cases
FROM cleaned_event_logs;

SELECT COUNT(DISTINCT activity) AS total_activities
FROM cleaned_event_logs;

SELECT
    activity,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY activity
ORDER BY event_count DESC;

SELECT
    case_id,
    COUNT(*) AS event_count
FROM cleaned_event_logs
GROUP BY case_id
ORDER BY event_count DESC;

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