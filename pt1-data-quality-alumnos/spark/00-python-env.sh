#!/bin/bash
# Este script debe ejecutarse al mismo nivel donde se tenga el script 01-limpieza-spark.ipynb
# También es necesario darle permisos con: chmod +x 00-python-env.sh
# Al finalizar se contará con el ambiente virtual creado,
# pero en caso de querer activarlo después se realizará con: source venv_spark/bin/activate
# Con el ambiente activado ahora si se puede abrir el notebook: jupyter lab 01-limpieza-spark.ipynb

echo "Iniciando instalación de ambiente..."

echo "Instalando soporte para entornos virtuales (python3-venv)..."
sudo apt install -y python3-venv

VENV_NAME="venv_spark"

# Crear entorno virtual
python3 -m venv $VENV_NAME

# Activar entorno
echo "Activando entorno virtual..."

echo "Actualizando pip dentro del entorno..."
pip install --upgrade pip

echo "Instalando librerías necesarias..."
pip install pyspark
pip install notebook ipykernel

# Registrar kernel en Jupyter
echo "Registrando kernel en Jupyter..."
python -m ipykernel install --user --name "$VENV_NAME" --display-name "PySpark Env"

echo "---------------------------------------"
echo "Entorno virtual listo!"
echo "Para activarlo de nuevo se usa: source venv/bin/$VENV_NAME"
echo ""
echo "Con el ambiente activado ya se puede ejecutar:"
echo "    02-limpieza-spark.ipynb"
echo "---------------------------------------"
