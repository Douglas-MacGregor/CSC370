SELECT
    gs1.machine_id AS machine_1,
    gs1.region_id AS region_1,
    gs2.machine_id AS machine_2,
    gs2.region_id AS region_2,
    gs1.gpu_type_name
FROM GPUServer AS gs1
JOIN GPUServer AS gs2 ON gs1.gpu_type_name = gs2.gpu_type_name
    AND gs1.region_id <> gs2.region_id
    AND gs1.machine_id < gs2.machine_id
WHERE gs1.gpu_type_name = 'V100';