SELECT machine_id
FROM GPUServer
WHERE NOT EXISTS (
    SELECT 1
    FROM InferenceRequest
    WHERE InferenceRequest.machine_id = GPUServer.machine_id
);