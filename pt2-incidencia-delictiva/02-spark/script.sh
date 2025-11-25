#!/bin/bash

# --- CONFIGURACIÓN ---
# Script de Python a ejecutar
PYTHON_SCRIPT="etl_spark.py"

# Versión del driver de Postgres (Compatible con Java 8/11/17)
PG_DRIVER_VERSION="42.7.3"
JAR_NAME="postgresql-${PG_DRIVER_VERSION}.jar"
JAR_URL="https://repo1.maven.org/maven2/org/postgresql/postgresql/${PG_DRIVER_VERSION}/${JAR_NAME}"

# --- 1. VERIFICACIÓN DEL DRIVER ---
echo "🔍 Verificando driver JDBC de PostgreSQL..."

if [ ! -f "$JAR_NAME" ]; then
    echo "⬇️  Driver no encontrado. Descargando $JAR_NAME..."
    if command -v wget &> /dev/null; then
        wget -q --show-progress "$JAR_URL"
    elif command -v curl &> /dev/null; then
        curl -O "$JAR_URL"
    else
        echo "❌ Error: Necesitas 'wget' o 'curl' instalado para descargar el driver automatically."
        exit 1
    fi
else
    echo "✅ Driver encontrado: $JAR_NAME"
fi

# --- 2. VERIFICACIÓN DE SPARK ---
if ! command -v spark-submit &> /dev/null; then
    echo "❌ Error: No se encontró 'spark-submit'. Asegúrate de que Spark está instalado y en tu PATH."
    exit 1
fi

# --- 3. EJECUCIÓN DEL ETL ---
echo "🚀 Iniciando Spark Submit..."
echo "--------------------------------"

spark-submit \
    --master "local[*]" \
    --driver-class-path "$JAR_NAME" \
    --jars "$JAR_NAME" \
    "$PYTHON_SCRIPT"

# Capturar el código de salida de Python
RET_CODE=$?

echo "--------------------------------"
if [ $RET_CODE -eq 0 ]; then
    echo "✅ El script finalizó correctamente."
else
    echo "❌ Hubo un error durante la ejecución."
fi
