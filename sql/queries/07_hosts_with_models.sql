SELECT
    h.machine_id,
    m.model_name
FROM Hosts
NATURAL JOIN AIModel;