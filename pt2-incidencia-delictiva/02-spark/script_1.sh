#!/usr/bin/env bash

# 🚨 CAMBIO DE ESTRATEGIA: NO USAR spark-submit
# Usar el interprete de Python dentro del Venv directamente
VENV_PYTHON="./venv_etl/bin/python"

echo "Iniciando proceso de limpieza de datos"

# Ejecutar el script Python con el intérprete del Venv
$VENV_PYTHON ETL_1.py

if [ $? -eq 0 ]; then
    echo "Limpieza completada."
else
    echo "Error en la limpieza."
    exit 1
fi
