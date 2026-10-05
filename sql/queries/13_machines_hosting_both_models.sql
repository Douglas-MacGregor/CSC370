SELECT machine_id
FROM Hosts
WHERE model_id = 1
INTERSECT
SELECT machine_id
FROM Hosts
WHERE model_id = 2;