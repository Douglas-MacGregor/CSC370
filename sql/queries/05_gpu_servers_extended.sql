SELECT
    gs.*,
    sgt.memory_gb,
    r.region_name,
    r.country
FROM GPUServer AS gs
JOIN GPUType AS gt ON gs.gpu_type_name = gt.gpu_type_name
JOIN SpecificGPUType AS sgt ON gs.gpu_type_name = sgt.gpu_type_name
JOIN Region AS r ON gs.region_id = r.region_id;