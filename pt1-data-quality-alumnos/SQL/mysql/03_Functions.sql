USE ING_DATOS;

DELIMITER $$

CREATE FUNCTION extract_and_normalize_state(location TEXT)
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    DECLARE result VARCHAR(100);
    DECLARE clean_location TEXT;

    IF location IS NULL OR TRIM(location) = '' THEN
        RETURN NULL;
    END IF;

    SET clean_location = REPLACE(location, 'Nací en ', '');
    SET clean_location = REPLACE(clean_location, ', antes D.F', '');
    SET clean_location = REPLACE(clean_location, 'México D.F -> ', '');
    SET clean_location = REPLACE(clean_location, ',Veracruz', ', Veracruz');

    SELECT sm.normalized_name INTO result
    FROM state_mapping sm
    WHERE clean_location LIKE CONCAT('%', sm.key_name, '%')
    LIMIT 1;

    RETURN result;
END$$


CREATE FUNCTION parse_spanish_date_fixed(date_str TEXT)
RETURNS DATE
DETERMINISTIC
BEGIN
    DECLARE s TEXT;

    IF date_str IS NULL OR TRIM(date_str) = '' THEN
        RETURN NULL;
    END IF;

    SET s = LOWER(TRIM(date_str));

    SET s = REGEXP_REPLACE(s, '\\bde\\b', ' ');
    SET s = REGEXP_REPLACE(s, '\\bdel\\b', ' ');

    SET s = REGEXP_REPLACE(s, '\\s+', ' ');

    SET s = REGEXP_REPLACE(s, 'enero|ene', '01');
    SET s = REGEXP_REPLACE(s, 'febrero|feb', '02');
    SET s = REGEXP_REPLACE(s, 'marzo|mar', '03');
    SET s = REGEXP_REPLACE(s, 'abril|abr', '04');
    SET s = REGEXP_REPLACE(s, 'mayo|may', '05');
    SET s = REGEXP_REPLACE(s, 'junio|jun', '06');
    SET s = REGEXP_REPLACE(s, 'julio|jul', '07');
    SET s = REGEXP_REPLACE(s, 'agosto|ago', '08');
    SET s = REGEXP_REPLACE(s, 'septiembre|sep', '09');
    SET s = REGEXP_REPLACE(s, 'octubre|oct', '10');
    SET s = REGEXP_REPLACE(s, 'noviembre|nov', '11');
    SET s = REGEXP_REPLACE(s, 'diciembre|dic', '12');

    SET s = REGEXP_REPLACE(s, '[\\.\\-\\s]', '/');

    RETURN STR_TO_DATE(s, '%d/%m/%Y');
END$$


CREATE FUNCTION extract_district_and_state_refined(location TEXT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE loc_clean TEXT;
    DECLARE district TEXT DEFAULT NULL;
    DECLARE state TEXT DEFAULT NULL;
    DECLARE found_state TEXT DEFAULT NULL;
    DECLARE found_key TEXT DEFAULT NULL;

    IF location IS NULL OR TRIM(location) = '' THEN
        RETURN NULL;
    END IF;

    
    SET loc_clean = TRIM(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                    REGEXP_REPLACE(LOWER(location),
                    'en ', ''),
            ', vivo solo', ''
            ),
        '\\s+', ' '
        )
    );

    SET loc_clean = REPLACE(loc_clean, 'coyoacan', 'coyoacán');

    IF REGEXP_LIKE(loc_clean, 'tizayuca\\s+hidalgo') THEN
        SET district = 'Tizayuca';
        SET state = 'Hidalgo';
        RETURN CONCAT(district, '|', state);
    END IF;

    SELECT sm.normalized_name, sm.key_name
    INTO found_state, found_key
    FROM state_mapping sm
    WHERE loc_clean LIKE CONCAT('%', LOWER(sm.key_name), '%')
    LIMIT 1;

    IF found_state IS NOT NULL THEN
        SET state = found_state;
    END IF;

    IF LOCATE(',', loc_clean) > 0 THEN
        SET district = TRIM(SUBSTRING_INDEX(loc_clean, ',', 1));
    ELSE
        IF found_key IS NOT NULL THEN
            SET district = TRIM(SUBSTRING_INDEX(loc_clean, found_key, 1));
        END IF;
    END IF;

    IF LOCATE('coyoacán', loc_clean) > 0 THEN
        SET district = 'Coyoacán';
        SET state = 'Ciudad de México';
    END IF;

    IF LOCATE('benito juárez', loc_clean) > 0 THEN
        SET district = 'Benito Juárez';
        SET state = 'Ciudad de México';
    END IF;

    IF LOCATE('chimalhuacán', loc_clean) > 0 THEN
        SET district = 'Chimalhuacán';
        SET state = 'Estado de México';
    END IF;

    IF LOCATE('ocoyoacac', loc_clean) > 0 THEN
        SET district = 'Ocoyoacac';
        SET state = 'Estado de México';
    END IF;

    IF state IS NULL AND loc_clean IS NOT NULL THEN
        SET district = TRIM(SUBSTRING_INDEX(loc_clean, ',', 1));
    END IF;

    RETURN CONCAT(IFNULL(district, ''), '|', IFNULL(state, ''));
END$$


CREATE FUNCTION clean_workplace(workplace TEXT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE cleaned TEXT;

    IF workplace IS NULL THEN
        RETURN NULL;
    END IF;

    
    SET cleaned = REGEXP_REPLACE(workplace, '(?i)Trabajo en\\s*', '');

    SET cleaned = REGEXP_REPLACE(cleaned, '(?i)una consultora llamada\\s*', '');

    
    SET cleaned = TRIM(SUBSTRING_INDEX(
        REGEXP_REPLACE(cleaned, '(?i)\\s+en\\s+', ' en '), 
        ' en ', 1
    ));
    SET cleaned = TRIM(SUBSTRING_INDEX(cleaned, ',', 1));
    SET cleaned = TRIM(SUBSTRING_INDEX(cleaned, '(', 1));

    IF cleaned = '' THEN
        RETURN NULL;
    END IF;

    RETURN cleaned;
END$$


CREATE FUNCTION number_of_residents(input_text TEXT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE txt_lower TEXT;
  DECLARE num INT;
  DECLARE match_somos TEXT;
  DECLARE match_contandome TEXT;
  DECLARE extracted_num INT;
  DECLARE result INT;

  SET txt_lower = LOWER(TRIM(input_text));

  SET num = CAST(REGEXP_SUBSTR(txt_lower, '[0-9]+') AS SIGNED);

  SET match_somos = REGEXP_SUBSTR(txt_lower, 'somos[[:space:]]*[0-9]+');
  SET match_contandome = REGEXP_SUBSTR(txt_lower, '[0-9]+[[:space:]]*personas[[:space:]]*contandome');

  IF match_somos IS NOT NULL THEN
    SET extracted_num = CAST(REGEXP_SUBSTR(match_somos, '[0-9]+') AS SIGNED);
  ELSEIF match_contandome IS NOT NULL THEN
    SET extracted_num = CAST(REGEXP_SUBSTR(match_contandome, '[0-9]+') AS SIGNED);
  ELSE
    SET extracted_num = NULL;
  END IF;

  SET result = CASE
    WHEN txt_lower LIKE '%vivo solo%' OR txt_lower LIKE '%nadie%' THEN 1
    WHEN extracted_num IS NOT NULL THEN extracted_num
    WHEN num IS NOT NULL THEN num + 1
    ELSE 1
  END;

  IF result < 1 THEN
    SET result = 1;
  END IF;

  RETURN result;
END$$


CREATE FUNCTION normalize_course_name(course_raw TEXT)
RETURNS TEXT
DETERMINISTIC
BEGIN
  DECLARE c TEXT;
  SET c = LOWER(TRIM(course_raw));

  IF c REGEXP 'admin[.]? de servicios de internet' THEN RETURN 'Administración de Servicios de Internet';
  ELSEIF c REGEXP 'administración de proyectos' THEN RETURN 'Administración de Proyectos de Software';
  ELSEIF c REGEXP 'bases de datos distribuidas' THEN RETURN 'Bases de Datos Distribuidas';
  ELSEIF c REGEXP 'bases de datos [(]todas[)]' THEN RETURN 'Bases de Datos';
  ELSEIF c REGEXP 'bases de datos' OR c REGEXP '\\bbd\\b' THEN RETURN 'Bases de Datos';
  ELSEIF c REGEXP 'cálculo y geo' OR c REGEXP 'calculo y geometria analitica' THEN RETURN 'Cálculo y Geometría Analítica';
  ELSEIF c REGEXP 'cálculo vectorial' THEN RETURN 'Cálculo Vectorial';
  ELSEIF c REGEXP 'minería de datos' THEN RETURN 'Minería de Datos';
  ELSEIF c REGEXP 'estadística' THEN RETURN 'Fundamentos de Estadística';
  ELSEIF c REGEXP 'poo' THEN RETURN 'Programación Orientada a Objetos';
  ELSEIF c REGEXP 'redes de datos seguras' OR c REGEXP 'cisco' THEN RETURN 'Redes de Datos Seguras';
  ELSEIF c REGEXP 'sistemas distribuidos' THEN RETURN 'Sistemas Distribuidos';
  ELSEIF c REGEXP 'sistemas operativos' THEN RETURN 'Sistemas Operativos';
  ELSEIF c REGEXP 'estructura de datos' THEN RETURN 'Estructura de Datos y Algoritmos I';
  ELSEIF c REGEXP 'eda2' THEN RETURN 'Estructura de Datos y Algoritmos II';
  ELSEIF c REGEXP 'dispositivos' THEN RETURN 'Dispositivos Electrónicos';
  ELSEIF c REGEXP 'lenguajes autómatas' THEN RETURN 'Lenguajes y Autómatas';
  ELSEIF c REGEXP 'taller socio' THEN RETURN 'Taller Sociohumanístico - Liderazgo';
  ELSE RETURN CONCAT(UCASE(LEFT(c,1)), SUBSTRING(c,2)); -- Capitaliza si no hay match
  END IF;
END$$


DELIMITER ;
