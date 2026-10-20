SELECT machine_id
FROM Hosts
WHERE model_id = 1
  AND machine_id IN (
      SELECT machine_id
      FROM Hosts
      WHERE model_id = 2
  );