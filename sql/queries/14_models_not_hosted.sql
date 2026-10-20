SELECT model_id
FROM AIModel
WHERE NOT EXISTS (
    SELECT 1
    FROM Hosts
    WHERE Hosts.model_id = AIModel.model_id
);