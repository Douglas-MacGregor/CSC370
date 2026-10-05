SELECT
    gs.machine_id,
    gs.gpu_type_name,
    mm.metric_id,
    mm.gpu_utilization,
    mm.cpu_utilization
FROM GPUServer AS gs
JOIN MachineMetric AS mm ON gs.machine_id = mm.machine_id
WHERE mm.gpu_utilization > mm.cpu_utilization + 100;