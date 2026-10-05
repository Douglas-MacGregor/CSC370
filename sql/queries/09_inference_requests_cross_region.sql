SELECT
    ir.request_id,
    ir.response_time_ms,
    gs.machine_id,
    server_r.region_name AS server_region,
    client_r.region_name AS client_region
FROM InferenceRequest AS ir
JOIN GPUServer AS gs ON ir.machine_id = gs.machine_id
JOIN Region AS server_r ON gs.region_id = server_r.region_id
JOIN Region AS client_r ON ir.region_id = client_r.region_id
WHERE ir.region_id <> gs.region_id;