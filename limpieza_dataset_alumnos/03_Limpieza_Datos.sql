USE ING_DATOS;

WITH
	name_cleaned AS (SELECT id, nombre AS name FROM STUDENT_DATA_RAW),
	edad_cleaned AS (SELECT id, REGEXP_REPLACE(edad, '\\D', '') AS age FROM STUDENT_DATA_RAW)
SELECT
	NC.id, name, age
FROM name_cleaned NC
INNER JOIN edad_cleaned EC
	ON NC.ID = EC.ID;
