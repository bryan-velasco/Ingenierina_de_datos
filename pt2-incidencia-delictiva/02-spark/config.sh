#!/usr/bin/env bash

# Usamos la ruta absoluta a python3 para asegurar que se use el sistema base
if [ ! -d "venv_etl" ]; then
    echo "Creando entorno virtual"
    /usr/bin/python3 -m venv venv_etl
fi

# ❌ NO DEBE EXISTIR: source "venv_etl/bin/activate"

# Definir la ruta de los ejecutables DENTRO del venv
VENV_PIP="./venv_etl/bin/pip"

echo "Instalando dependencias"
# 🚨 DEBES USAR LA VARIABLE VENV_PIP. ¡CRÍTICO!
$VENV_PIP install pyspark

JAR_NAME="postgresql-42.7.3.jar"
if [ ! -f "$JAR_NAME" ]; then
    echo "Descargando Driver PostgreSQL"
    wget -q "https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/$JAR_NAME"
fi

echo "Configuracion finalizada"
