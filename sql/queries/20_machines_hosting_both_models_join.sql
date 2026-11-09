-- Join formulation of query 13
-- This removes the IN subquery while keeping the same requested result
SELECT h1.machine_id
FROM Hosts AS h1
JOIN Hosts AS h2 ON h1.machine_id = h2.machine_id
WHERE h1.model_id = 1
    AND h2.model_id = 2;

-- query 13:
-- SELECT machine_id
-- FROM Hosts
-- WHERE model_id = 1
--   AND machine_id IN (
--       SELECT machine_id
--       FROM Hosts
--       WHERE model_id = 2
--   );