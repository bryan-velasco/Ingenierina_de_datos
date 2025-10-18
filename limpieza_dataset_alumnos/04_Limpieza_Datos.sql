USE ING_DATOS;

WITH
	name_cleaned AS (SELECT id, nombre AS name FROM STUDENT_DATA_RAW),
	edad_cleaned AS (SELECT id, REGEXP_REPLACE(edad, '\\D', '') AS age FROM STUDENT_DATA_RAW),
	state_of_birth_cleaned AS (SELECT id, extract_and_normalize_state(lugar_nacimiento) AS state_of_birth FROM STUDENT_DATA_RAW),
	grade_cleaned AS (SELECT id, REGEXP_SUBSTR(REPLACE(Promedio, ',', '.'), '[0-9]+\\.?[0-9]*') AS grade_average FROM STUDENT_DATA_RAW),
	date_of_birth_cleaned AS (SELECT id, parse_spanish_date_fixed(fecha_nacimiento) AS date_of_birth FROM STUDENT_DATA_RAW),
	current_district_cleaned AS (SELECT id, donde_vivo, SUBSTRING_INDEX(extract_district_and_state_refined(donde_vivo), '|', 1) AS current_district FROM STUDENT_DATA_RAW),
	current_state_cleaned AS (SELECT id, donde_vivo, SUBSTRING_INDEX(extract_district_and_state_refined(donde_vivo), '|', -1) AS current_state FROM STUDENT_DATA_RAW)
	-- Trabajo
	
SELECT
	NC.id,
	NC.name,
	EC.age ,
	SOBC.state_of_birth,
	GC.grade_average,
	DOBC.date_of_birth,
	CDC.current_district,
	CSC.current_state

FROM name_cleaned NC
INNER JOIN edad_cleaned EC USING (ID)
INNER JOIN state_of_birth_cleaned SOBC USING (ID)
INNER JOIN grade_cleaned GC USING (ID)
INNER JOIN date_of_birth_cleaned DOBC USING (ID)
INNER JOIN current_district_cleaned CDC USING (ID)
INNER JOIN current_state_cleaned CSC USING (ID);