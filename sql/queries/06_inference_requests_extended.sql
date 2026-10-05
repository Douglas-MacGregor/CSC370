SELECT 
    ir.request_id,
    ir.response_time_ms,
    m.model_name,
    r.region_name,
    r.country
FROM InferenceRequest AS ir
JOIN AIModel as m ON ir.model_id = m.model_id
JOIN Region as r ON ir.region_id = r.region_id;