SELECT
    h.machine_id,
    m.model_name
FROM Hosts AS h
JOIN AIModel AS m ON h.model_id = m.model_id;