SELECT model_id
FROM AIModel
EXCEPT
SELECT model_id
FROM Hosts;