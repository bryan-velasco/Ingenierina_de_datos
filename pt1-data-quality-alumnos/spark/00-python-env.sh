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

if [ ! -d "$VENV_NAME" ]; then
    echo "Creando entorno virtual '$VENV_NAME'..."
    python3 -m venv $VENV_NAME
else
    echo "Ya existe un entorno virtual llamado '$VENV_NAME'."
fi

echo "Creando entorno virtual..."


echo "Activando entorno virtual..."
source $VENV_NAME/bin/activate

echo "Actualizando pip dentro del entorno..."
pip install --upgrade pip

echo "Instalando librerías necesarias dentro del venv..."
pip install pyspark
pip install notebook ipykernel

echo "Registrando kernel en Jupyter..."
python -m ipykernel install --user --name "$VENV_NAME" --display-name "PySpark Env"

echo "---------------------------------------"
echo "Entorno virtual listo!"
echo ""
echo "Para activarlo nuevamente usa:"
echo "   source $VENV_NAME/bin/activate"
echo ""
echo "Con el ambiente activado ya se pueden usar los notebook:"
echo "   jupyter notebook"
echo "   jupyter lab"
echo "   jupyter lab 01-limpieza-spark.ipynb"
echo "---------------------------------------"

