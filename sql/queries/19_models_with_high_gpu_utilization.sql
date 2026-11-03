-- EXISTS subquery with aggregation
-- A model is returned when at least one server hosting it has high average GPU utilization
SELECT
    m.model_id,
    m.model_name
FROM AIModel AS m
WHERE EXISTS (
    SELECT 1
    FROM Hosts AS h
    JOIN MachineMetric AS mm ON h.machine_id = mm.machine_id
    WHERE h.model_id = m.model_id
        AND mm.gpu_utilization IS NOT NULL
    GROUP BY h.machine_id
    HAVING AVG(mm.gpu_utilization) > 100
);