USE ING_DATOS;

INSERT INTO state_mapping (key_name, normalized_name)
VALUES
('CDMX', 'Ciudad de México'),
('D.F', 'Ciudad de México'),
('Ciudad de México', 'Ciudad de México'),
('Edo. Méx', 'Estado de México'),
('Estado de México', 'Estado de México'),
('Veracruz', 'Veracruz'),
('Oaxaca', 'Oaxaca'),
('Hidalgo', 'Hidalgo');


INSERT INTO STUDENT_DATA_RAW
    (nombre, edad, lugar_nacimiento, promedio, fecha_nacimiento, donde_vivo, trabajo, donde_trabajo, semestre, def_ingenieria, def_dato, artista_favorito, hobbies, con_cuantos_vivo, materias_favoritas)
VALUES
('Aldo Abad Vásquez', '25', 'Camerino Z. Mendoza,Veracruz', '8.78', '23 de octubre de 1999', 'Copilco El Alto, Coyoacán, CDMX', 'No', '', 'Ya debería haber terminado', 'La aplicación de conocimientos y técnicas a un fin.', 'La unidad mínima de información.', 'Ado', 'Tocar guitarra, cocinar y modding de Minecraft', '7', 'Bases de Datos Distribuidas, Minería de Datos y Taller Socio-humanístico: Liderazgo'),
('Guillermo Hernandez Ruiz de Esparza', '22', 'CDMX', '8.5', '8 de octubre de 2002', 'Coyoacan', 'No', '', '9', 'Conjunto de conocimientos y tecnicas para solucionar un problema', 'Conjunto de informacion que tiene un contexto y significado', 'Maneskin', 'Ver deportes, escuchar musica, ver peliculas', '', 'Diseño digial moderno, bases de datos, algebra'),
('Bryan Velasco Pachuca', '24', 'Nací en milpalta, CDMX', '9.21', '28 de abril de 2001', 'En Coyoacán', 'Si', 'Trabajo en una consultora llamada Motivus, con Grupo Infra', 'En 13° semestre', 'Es la aplicación de estándares calidad y tecnología a la resolución de problemas', 'Es la representación de un valor o descripción de alguna magnitud, cosa, concepto o persona', 'Kali Uchis, Caravan Palace, Disclosure', 'Salir en moto, patinar y leer', '0 personas, vivo solo', 'POO, Cálculo y Geo., Admin. de servicios de internet'),
('Dulce Michelle Barrios Aguilar', '22  años', 'Nací en CDMX, antes D.F', '8.55 hasta el momento', '31 de enero de 2003', 'Venustiano Carranza, CDMX', 'Si', 'Trabajo en IBM', 'Noveno semestre (8°,9°,10°)', 'Conjunto de habilidades y conocimientos aplicados para innovar, crear, mantener y diseñar un proceso, un sistema, etc.', 'Hecho que tiene relevancia implícita para cierto rubro', 'Twenty One Pilots y Cage the Elephant', 'Nadar, conocer lugares nuevos y descubrir nueva música', '4 personas contandome a mi ', 'Estadística, Bases de Datos, Administración de proyectos, Sistemas Distribuidos'),
('Carlos Enrique Figueroa Solano', '21', 'Xalapa, Veracruz', '9', '11/10/2003', 'Coyoacán', 'Si', 'Bimbo', '9no', 'Es la ciencia de resolver problemas', 'Es la parte más pequeña de la información', 'Nothing But Thieves', 'Fotografía, videojuegos, escuchar música', '2', 'Cálculo Vectorial, Estructura de datos y algoritmos, dispositivos'),
('Gómez Urbano Mariana', '22 años', 'Edo. Méx, Chimalhuacán', '8.9', '06/nov/2022', 'Chimalhuacán', 'No', '', '10', 'Disciplina que engloba múltiples conocimientos técnicos y científicos con el fin de diseñar e implementar soluciones innovadoras', 'Es una representación de sucesos, carácteristicas; por lo regular un dato no tiene significado por si solo necesita ser tratado para llegar a ser información', 'Miku', 'Ver series, leer manwas, salir a caminar', 'En copilco somos 2, en mi casa 5', ''),
('Jonathan Reyes Ramírez', '25 años', 'Estado de México', '8.8', '26 de marzo del 2000', 'Ocoyoacac, Estado de México', 'No', '', '11vo semestre', 'Es el "arte" o forma en que conocimiento teorico se lleva a la practica, ya sea para solucionar un problema, innovar o crear tecnología', 'Es información que puede estar guardada en diferentes formatos y que nos sirve para entender algo', 'Royal Blod', 'Ver películas, Escuchar musica, caminar/correr por la naturaleza', '3', 'Calculo y Geometría analítica, Sistemas de comunicaciones. Sistemas operativos'),
('Carlos Ceniceros Moriaca', '23', 'Ciudad de México', '8.56', '24 de agosto de 2001', 'Tizayuca Hidalgo', 'No trabajo', '', 'Estoy en mi onceavo semestre', 'La disciplina encargada de aplicar la teoría en beneficio de un fin', 'La unidad minima de la información', 'Sabatan', 'Descansar, ver peliculas, jugar videojuegos', '3', 'Bases de datos, Redes de Datos seguras, EDA2'),
('Ernesto Quintana López', '22 años', 'Tuxtepec, Oaxaca', '9.1', '6/Diciembre/2002', 'Coyoacan', 'No', '', '9', 'El conocimiento que se utiliza para realizar cosas con ingenio', 'Representación de un pequeño fragmento de información', 'Cuarteto de Nos', 'Correr,Escuchar musica y cocinar', 'Nadie', 'POO,Calculo y Geometria Analitica y BD'),
('Laylet Rojas Terrazas', '26 años ', 'México D.F -> CDMX', '9.65', '19 de octubre de 1998', 'Benito Juárez ', 'Si', 'Trabajo en PepsiCo en CMDB, "Data Governance"', 'Onceavo semestre', 'Conjunto de Ciencias aplicadas para diseñar, construir soluciones óptimas y facilitar la vida ', 'Mínima información, por si solo no tiene significado', 'Coldplay ', 'Tocar piano, hacer ejercicio (artes mixtas), cocinar ', '3 personas más ', 'Bases de datos (todas), Cisco, cálculo y geometriía analítica, lenguajes autómatas ');
