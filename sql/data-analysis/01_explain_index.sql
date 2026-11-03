-- Compare the aggregation query before and after adding a non-primary index
-- The index is removed at the end so this analysis script can be rerun safely
EXPLAIN
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

CREATE INDEX idx_inference_response_time
ON InferenceRequest(response_time_ms);

EXPLAIN
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

DROP INDEX idx_inference_response_time
ON InferenceRequest;