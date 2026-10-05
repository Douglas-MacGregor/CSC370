SELECT 
    ir.request_id,
    ir.response_time_ms,
    m.model_name
FROM InferenceRequest AS ir
JOIN AIModel as m ON ir.model_id = m.model_id
WHERE ir.response_time_ms > 1000000;