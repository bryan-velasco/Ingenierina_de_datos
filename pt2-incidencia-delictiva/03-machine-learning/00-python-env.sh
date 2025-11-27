#!/bin/bash
# Este script debe ejecutarse al mismo nivel donde se tenga el script 01-prediccion_incidencia_delictiva.py
# Uso:
#    chmod +x 00-python-env.sh
#    ./00-python-env.sh
#
# Al finalizar se contará con el ambiente virtual creado,
# pero en caso de querer activarlo manualmente ejecutar lo siguiente:
#    source venv_ml/bin/activate


echo "Iniciando instalación de ambiente para ML..."

# 1. Asegurar que python3-venv está instalado
echo "Instalando soporte para entornos virtuales (python3-venv)..."
sudo apt install -y python3-venv

VENV_NAME="venv_ml"

# 2. Crear entorno virtual
if [ ! -d "$VENV_NAME" ]; then
    echo "Creando entorno virtual '$VENV_NAME'..."
    python3 -m venv $VENV_NAME
else
    echo "El entorno virtual '$VENV_NAME' ya existe."
fi

# 3. Activar entorno virtual
echo "Activando entorno virtual..."
source $VENV_NAME/bin/activate

# 4. Actualizar pip
echo "Actualizando pip dentro del entorno..."
pip install --upgrade pip

# 5. Instalar librerías necesarias
echo "Instalando librerías necesarias para ML..."
pip install pandas
pip install numpy
pip install matplotlib
pip install scikit-learn

echo "---------------------------------------"
echo "   Entorno virtual para ML listo!"
echo "---------------------------------------"
echo ""
echo "Para activarlo manualmente usa:"
echo "   source $VENV_NAME/bin/activate"
echo ""
echo "---------------------------------------"