#!/usr/bin/env bash

# 🚨 CAMBIO DE ESTRATEGIA: NO USAR spark-submit
VENV_PYTHON="./venv_etl/bin/python"

echo "Iniciando carga a Base de Datos"

# Ejecutar el script Python con el intérprete del Venv
$VENV_PYTHON ETL_2.py

if [ $? -eq 0 ]; then
    echo "Carga a BD completada."
else
    echo "Error en la carga."
    exit 1
fi
