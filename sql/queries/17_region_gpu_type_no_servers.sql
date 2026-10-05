SELECT r.region_id, gt.gpu_type_name
FROM Region AS r
CROSS JOIN GPUType AS gt
EXCEPT
SELECT region_id, gpu_type_name
FROM GPUServer;