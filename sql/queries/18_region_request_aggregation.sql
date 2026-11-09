-- aggregation
-- region_id functionally determines region_name and country, so we group only by region_id
SELECT
    r.region_id,
    r.region_name,
    r.country,
    COUNT(*) AS request_count,
    AVG(ir.response_time_ms) AS average_response_time_ms
FROM Region AS r
JOIN InferenceRequest AS ir ON r.region_id = ir.region_id
WHERE ir.response_time_ms > 1000000
GROUP BY r.region_id
HAVING COUNT(*) >= 5;