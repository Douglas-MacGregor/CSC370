SELECT machine_id
FROM GPUServer
EXCEPT
SELECT machine_id
FROM InferenceRequest;