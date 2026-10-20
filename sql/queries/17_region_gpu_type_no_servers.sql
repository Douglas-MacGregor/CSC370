SELECT r.region_id, gt.gpu_type_name
FROM Region AS r
CROSS JOIN GPUType AS gt
WHERE NOT EXISTS (
    SELECT 1
    FROM GPUServer AS gs
    WHERE gs.region_id = r.region_id
      AND gs.gpu_type_name = gt.gpu_type_name
);