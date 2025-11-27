USE ING_DATOS;

WITH
	name_cleaned AS (SELECT id, nombre AS name FROM STUDENT_DATA_RAW),
	edad_cleaned AS (SELECT id, REGEXP_REPLACE(edad, '\\D', '') AS age FROM STUDENT_DATA_RAW),
	state_of_birth_cleaned AS (SELECT id, extract_and_normalize_state(lugar_nacimiento) AS state_of_birth FROM STUDENT_DATA_RAW),
	grade_cleaned AS (SELECT id, REGEXP_SUBSTR(REPLACE(Promedio, ',', '.'), '[0-9]+\\.?[0-9]*') AS grade_average FROM STUDENT_DATA_RAW),
	date_of_birth_cleaned AS (SELECT id, parse_spanish_date_fixed(fecha_nacimiento) AS date_of_birth FROM STUDENT_DATA_RAW),
	current_district_cleaned AS (SELECT id, donde_vivo, SUBSTRING_INDEX(extract_district_and_state_refined(donde_vivo), '|', 1) AS current_district FROM STUDENT_DATA_RAW),
	current_state_cleaned AS (SELECT id, donde_vivo, SUBSTRING_INDEX(extract_district_and_state_refined(donde_vivo), '|', -1) AS current_state FROM STUDENT_DATA_RAW),
	is_working_cleaned AS
		(
			SELECT
				id,
				CASE
					WHEN trabajo = 'Si' THEN 1
					WHEN trabajo IN ('No', 'No trabajo') THEN 0
					ELSE 0
				END AS is_working
			FROM STUDENT_DATA_RAW
		),
	workplace_cleaned AS (SELECT id, clean_workplace(donde_trabajo) AS workplace FROM STUDENT_DATA_RAW),
	semester_cleaned AS
		(
			SELECT 
			id,
			semestre,
			CASE
				WHEN LOWER(semestre) LIKE '%ya debería haber terminado%' THEN 11
				WHEN LOWER(semestre) LIKE '%noveno%' THEN 9
				WHEN LOWER(semestre) LIKE '%onceavo%' OR LOWER(semestre) LIKE '%11vo%' THEN 11
				WHEN REGEXP_SUBSTR(semestre, '[0-9]+') IS NOT NULL THEN 
					CASE 
						WHEN CAST(REGEXP_SUBSTR(semestre, '[0-9]+') AS UNSIGNED) > 10 THEN 11
						ELSE CAST(REGEXP_SUBSTR(semestre, '[0-9]+') AS UNSIGNED)
					END
				ELSE NULL
			END AS semester
		FROM STUDENT_DATA_RAW
		),
	engineering_definition_cleaned AS (SELECT id, def_ingenieria AS engineering_definition FROM STUDENT_DATA_RAW),
	data_definition_cleaned AS (SELECT id, def_dato AS data_definition FROM STUDENT_DATA_RAW),
	favorite_artist_cleaned AS (SELECT id, artista_favorito AS favorite_artist FROM STUDENT_DATA_RAW),
	hobbies_cleaned AS
	(
		SELECT
			id,
			hobbies,
			TRIM(REGEXP_SUBSTR(REPLACE(REPLACE(hobbies, ' y ', ', '), ' Y ', ', '), '[^,]+', 1, 1)) AS hobbie_1,
			TRIM(REGEXP_SUBSTR(REPLACE(REPLACE(hobbies, ' y ', ', '), ' Y ', ', '), '[^,]+', 1, 2)) AS hobbie_2,
			TRIM(REGEXP_SUBSTR(REPLACE(REPLACE(hobbies, ' y ', ', '), ' Y ', ', '), '[^,]+', 1, 3)) AS hobbie_3
		FROM STUDENT_DATA_RAW
	),
	number_of_residents_cleaned AS (SELECT id, number_of_residents(con_cuantos_vivo) AS number_of_residents FROM STUDENT_DATA_RAW),
	favorite_course_cleaned AS (SELECT
		id,
		normalize_course_name(TRIM(SUBSTRING_INDEX(materias_favoritas, ',', 1))) AS favorite_course_1,
		normalize_course_name(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(materias_favoritas, ',', 2), ',', -1))) AS favorite_course_2,
		normalize_course_name(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(materias_favoritas, ',', 3), ',', -1))) AS favorite_course_3
	FROM STUDENT_DATA_RAW)
	
SELECT
	NC.id,
	NC.name,
	EC.age ,
	SOBC.state_of_birth,
	GC.grade_average,
	DOBC.date_of_birth,
	CDC.current_district,
	CSC.current_state,
	IWC.is_working,
	WC.workplace,
	SC.semester,
	EDC.engineering_definition,
	DDC.data_definition,
	FAC.favorite_artist,
	HC.hobbie_1,
	HC.hobbie_2,
	HC.hobbie_3,
	NORC.number_of_residents,
	FCC.favorite_course_1,
	FCC.favorite_course_2,
	FCC.favorite_course_3
FROM name_cleaned NC
INNER JOIN edad_cleaned EC USING (ID)
INNER JOIN state_of_birth_cleaned SOBC USING (ID)
INNER JOIN grade_cleaned GC USING (ID)
INNER JOIN date_of_birth_cleaned DOBC USING (ID)
INNER JOIN current_district_cleaned CDC USING (ID)
INNER JOIN current_state_cleaned CSC USING (ID)
INNER JOIN is_working_cleaned IWC USING (ID)
INNER JOIN workplace_cleaned WC USING (ID)
INNER JOIN semester_cleaned SC USING (ID)
INNER JOIN engineering_definition_cleaned EDC USING (ID)
INNER JOIN data_definition_cleaned DDC USING (ID)
INNER JOIN favorite_artist_cleaned FAC USING (ID)
INNER JOIN hobbies_cleaned HC USING (ID)
INNER JOIN number_of_residents_cleaned NORC USING (ID)
INNER JOIN favorite_course_cleaned FCC USING (ID)
