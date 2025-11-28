#!/usr/bin/env bash

# 🚨 FIX: Usamos la ruta ABSOLUTA para el intérprete de Python del Venv.
VENV_PYTHON="/shared_data/pt2-incidencia-delictiva/02-spark/venv_etl/bin/python"

echo "Iniciando proceso de limpieza de datos"

# Ejecutar el script Python con el intérprete del Venv
$VENV_PYTHON ETL_1.py

if [ $? -eq 0 ]; then
    echo "Limpieza completada."
else
    echo "Error en la limpieza."
    exit 1
fi
