USE ING_DATOS;

CREATE TABLE STUDENT_DATA_RAW (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    edad VARCHAR(50),
    lugar_nacimiento VARCHAR(100),
    promedio VARCHAR(50),
    fecha_nacimiento VARCHAR(50),
    donde_vivo VARCHAR(100),
    trabajo VARCHAR(20),
    donde_trabajo VARCHAR(100),
    semestre VARCHAR(50),
    def_ingenieria VARCHAR(150),
    def_dato VARCHAR(200),
    artista_favorito VARCHAR(70),
    hobbies VARCHAR(100),
    con_cuantos_vivo VARCHAR(50),
    materias_favoritas VARCHAR(100)
);
