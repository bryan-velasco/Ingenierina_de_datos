#!/usr/bin/env bash

# 🔑 FIX 1: Usamos la ruta ABSOLUTA para el intérprete de Python del Venv.
VENV_PYTHON="/shared_data/pt2-incidencia-delictiva/02-spark/venv_etl/bin/python"

echo "Iniciando carga a Base de Datos"

# 🔑 FIX 2: Exportar la variable para cargar el driver JAR al iniciar Spark.
JAR_PATH="/shared_data/pt2-incidencia-delictiva/02-spark/postgresql-42.7.3.jar"
export PYSPARK_SUBMIT_ARGS="--jars $JAR_PATH pyspark-shell"

# Ejecutar el script Python con el intérprete del Venv
$VENV_PYTHON ETL_2.py

if [ $? -eq 0 ]; then
    echo "Carga a BD completada."
else
    echo "Error en la carga."
    exit 1
fi
