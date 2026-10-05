SELECT h.model_id, h.machine_id, gs.gpu_type_name
FROM Hosts AS h
JOIN GPUServer AS gs ON h.machine_id = gs.machine_id
EXCEPT
SELECT h.model_id, h.machine_id, gs.gpu_type_name
FROM Hosts AS h
JOIN GPUServer AS gs ON h.machine_id = gs.machine_id
JOIN CompatibleWith AS cw ON h.model_id = cw.model_id
    AND gs.gpu_type_name = cw.gpu_type_name;