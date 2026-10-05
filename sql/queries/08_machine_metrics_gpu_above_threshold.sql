SELECT
    gs.gpu_capacity,
    gs.gpu_type_name,
    mm.*
FROM GPUServer AS gs
JOIN MachineMetric AS mm ON gs.machine_id = mm.machine_id
WHERE mm.gpu_utilization > 250.0
    AND gs.machine_id = '0ada2343597a34b8ab9a3d00';