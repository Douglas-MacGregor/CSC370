-- Demonstrate INSERT and DELETE with complex query predicates without changing the core project data
-- The temporary table exists only for this MySQL session
CREATE TEMPORARY TABLE Sprint3CandidateServer(
    machine_id VARCHAR(100) PRIMARY KEY,
    average_gpu_utilization DOUBLE
);

-- Insert servers selected using aggregation and HAVING
INSERT INTO Sprint3CandidateServer(machine_id, average_gpu_utilization)
SELECT machine_id, AVG(gpu_utilization)
FROM MachineMetric
WHERE gpu_utilization IS NOT NULL
GROUP BY machine_id
HAVING AVG(gpu_utilization) > 100;

-- Deletes candidates that do not have at least four GPUs
DELETE FROM Sprint3CandidateServer
WHERE machine_id IN (
    SELECT machine_id
    FROM GPUServer
    WHERE gpu_capacity < 4
);

SELECT *
FROM Sprint3CandidateServer;