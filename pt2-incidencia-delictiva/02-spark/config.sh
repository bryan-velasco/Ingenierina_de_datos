#!/usr/bin/env bash

if [ ! -d "venv_etl" ]; then
    echo "Creando entorno virtual"
    python3 -m venv venv_etl
fi

source "venv_etl/bin/activate"
echo "Instalando dependencias"
python3 -m pip install pyspark

JAR_NAME="postgresql-42.7.3.jar"
if [ ! -f "$JAR_NAME" ]; then
    echo "Descargando Driver PostgreSQL"
    wget -q "https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/$JAR_NAME"
fi

echo "Configuracion finalizada"