-- Return a model when at least one server hosting it has high average GPU
-- utilization. Aggregate each model/server pair once, then remove duplicate
-- models that have multiple qualifying servers.
SELECT DISTINCT
    m.model_id,
    m.model_name
FROM AIModel AS m
JOIN Hosts AS h ON h.model_id = m.model_id
JOIN MachineMetric AS mm ON mm.machine_id = h.machine_id
WHERE mm.gpu_utilization IS NOT NULL
GROUP BY m.model_id, m.model_name, h.machine_id
HAVING AVG(mm.gpu_utilization) > 100;