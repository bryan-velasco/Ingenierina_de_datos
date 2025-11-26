#!/usr/bin/env bash

JAR_NAME="postgresql-42.7.3.jar"

source "venv_etl/bin/activate"

echo "Iniciando carga a Base de Datos"

spark-submit \
  --master "local[*]" \
  --driver-class-path "$JAR_NAME" \
  --jars "$JAR_NAME" \
  ETL_2.py

if [ $? -eq 0 ]; then
    echo "Carga a BD completada."
else
    echo "Error en la carga."
    exit 1
fi