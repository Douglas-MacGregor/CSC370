SELECT h.model_id, h.machine_id, gs.gpu_type_name
FROM Hosts AS h
JOIN GPUServer AS gs ON h.machine_id = gs.machine_id
WHERE NOT EXISTS (
    SELECT 1
    FROM CompatibleWith AS cw
    WHERE cw.model_id = h.model_id
      AND cw.gpu_type_name = gs.gpu_type_name
);