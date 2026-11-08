SELECT DISTINCT gs.gpu_type_name, sgt.memory_gb
FROM GPUServer AS gs
JOIN SpecificGPUType AS sgt ON gs.gpu_type_name = sgt.gpu_type_name;
