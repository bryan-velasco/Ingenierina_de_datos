#!/usr/bin/env bash

# Usamos la ruta absoluta a python3 para asegurar que se use el sistema base
if [ ! -d "venv_etl" ]; then
    echo "Creando entorno virtual"
    /usr/bin/python3 -m venv venv_etl # <-- Esto crea la carpeta venv_etl
fi

# ❌ NO DEBE EXISTIR: source "venv_etl/bin/activate"

# 🔑 FIX 1: Definir la ruta del intérprete de Python dentro del venv (ruta relativa estable)
VENV_PYTHON="./venv_etl/bin/python" 

echo "Instalando dependencias"
# 🔑 FIX 2: Usar el intérprete del Venv para ejecutar pip como un módulo. ¡Máxima estabilidad!
$VENV_PYTHON -m pip install pyspark

JAR_NAME="postgresql-42.7.3.jar"
JAR_URL="https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/$JAR_NAME"

if [ ! -f "$JAR_NAME" ]; then
    echo "Descargando Driver PostgreSQL con curl"
    # 🔑 FIX 3: Usamos curl para la descarga (opciones: -sSL silencioso, -o guarda el archivo)
    curl -sSL "$JAR_URL" -o "$JAR_NAME"
fi

echo "Configuracion finalizada"
