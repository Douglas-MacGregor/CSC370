SELECT DISTINCT gpu_type_name, memory_gb
FROM GPUServer AS gs
JOIN GPUType AS gt ON gs.gpu_type_name = gt.gpu_type_name;
