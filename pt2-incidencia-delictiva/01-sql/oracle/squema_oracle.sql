CREATE TABLE ESTADO (
    id_estado NUMBER(3) PRIMARY KEY,
    entidad VARCHAR2(100) NOT NULL
);

CREATE TABLE BIEN_AFECTADO (
    id_bien_afectado NUMBER(3) PRIMARY KEY,
    descripcion VARCHAR2(100)
);

CREATE TABLE TIPO_DELITO (
    id_tipo_delito NUMBER(5) PRIMARY KEY,
    descripcion VARCHAR2(100)
);

CREATE TABLE SUBTIPO_DELITO (
    id_subtipo_delito NUMBER(5) PRIMARY KEY,
    descripcion VARCHAR2(100)
);

CREATE TABLE MODALIDAD (
    id_modalidad NUMBER(5) PRIMARY KEY,
    descripcion VARCHAR2(100)
);

CREATE TABLE INDICE_ESTATAL_DELITO (
    id_indice_estatal_delito NUMBER(10) PRIMARY KEY,
    fecha_delito DATE NOT NULL,
    incidencia_delictiva NUMBER(10) NOT NULL,
    id_estado NUMBER(3) NOT NULL,
    id_bien_afectado NUMBER(3) NOT NULL,
    id_tipo_delito NUMBER(5) NOT NULL,
    id_subtipo_delito NUMBER(5) NOT NULL,
    id_modalidad NUMBER(5) NOT NULL,
    FOREIGN KEY (id_estado) REFERENCES ESTADO(id_estado),
    FOREIGN KEY (id_bien_afectado) REFERENCES BIEN_AFECTADO(id_bien_afectado),
    FOREIGN KEY (id_tipo_delito) REFERENCES TIPO_DELITO(id_tipo_delito),
    FOREIGN KEY (id_subtipo_delito) REFERENCES SUBTIPO_DELITO(id_subtipo_delito),
    FOREIGN KEY (id_modalidad) REFERENCES MODALIDAD(id_modalidad)
);
