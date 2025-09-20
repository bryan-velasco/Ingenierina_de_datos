CREATE TABLE ESTADO(
	id_estado TINYINT PRIMARY KEY,
	entidad VARCHAR(100) NOT NULL
);

CREATE TABLE BIEN_AFECTADO(
  	id_bien_afectado TINYINT PRIMARY KEY,
  	descripcion VARCHAR(100)
);

CREATE TABLE TIPO_DELITO(
  	id_tipo_delito SMALLINT PRIMARY KEY,
  	descripcion VARCHAR(100)
);

CREATE TABLE SUBTIPO_DELITO(
  	id_subtipo_delito SMALLINT PRIMARY KEY,
  	descripcion VARCHAR(100)
);

CREATE TABLE MODALIDAD(
  	id_modalidad SMALLINT PRIMARY KEY,
  	descripcion VARCHAR(100)
);

CREATE TABLE INDICE_ESTATAL_DELITO(
	id_indice_estatal_delito INT PRIMARY KEY,
  	fecha_delito DATE NOT NULL,
  	incidencia_delictiva INT NOT NULL,
  	id_estado TINYINT NOT NULL,
  	id_bien_afectado TINYINT NOT NULL,
  	id_tipo_delito SMALLINT NOT NULL,
  	id_subtipo_delito SMALLINT NOT NULL,
  	id_modalidad SMALLINT NOT NULL,
  	FOREIGN KEY (id_estado) REFERENCES ESTADO(id_estado),
  	FOREIGN KEY (id_bien_afectado) REFERENCES BIEN_AFECTADO(id_bien_afectado),
  	FOREIGN KEY (id_tipo_delito) REFERENCES TIPO_DELITO(id_tipo_delito),
  	FOREIGN KEY (id_subtipo_delito) REFERENCES SUBTIPO_DELITO(id_subtipo_delito),
  	FOREIGN KEY (id_modalidad) REFERENCES MODALIDAD(id_modalidad)
);

