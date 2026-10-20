SELECT machine_id
FROM GPUServer
WHERE region_id = 1
UNION
SELECT machine_id
FROM GPUServer
WHERE GPUServer.gpu_type_name = 'V100M32';