SELECT DISTINCT gs.gpu_type_name, sgt.memory_gb
FROM GPUServer AS gs
JOIN GPUType AS gt ON gs.gpu_type_name = gt.gpu_type_name
JOIN SpecificGPUType AS sgt ON gs.gpu_type_name = sgt.gpu_type_name;
