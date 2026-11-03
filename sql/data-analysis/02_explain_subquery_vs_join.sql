-- Compare the original subquery from query 13 with the equivalent join formulation.
EXPLAIN
SELECT machine_id
FROM Hosts
WHERE model_id = 1
    AND machine_id IN (
        SELECT machine_id
        FROM Hosts
        WHERE model_id = 2
    );

EXPLAIN
SELECT h1.machine_id
FROM Hosts AS h1
JOIN Hosts AS h2 ON h1.machine_id = h2.machine_id
WHERE h1.model_id = 1
    AND h2.model_id = 2;