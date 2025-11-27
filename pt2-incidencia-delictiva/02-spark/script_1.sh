#!/usr/bin/env bash

source "venv_etl/bin/activate"

echo "Iniciando proceso de limpieza de datos"

spark-submit \
  --master "local[*]" \
  ETL_1.py

if [ $? -eq 0 ]; then
    echo "Limpieza completada."
else
    echo "Error en la limpieza."
    exit 1
fi