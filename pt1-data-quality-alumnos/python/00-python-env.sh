#!/bin/bash
# Este script debe ejecutarse al mismo nivel donde se tenga el script 02 de limpieza
# También es necesario darle permisos con: chmod +x setup_etl.sh
# Al finalizar se contará con el ambiente virtual creado,
# pero en caso de querer activarlo después se realizará con: source venv/bin/activate
# Con el ambiente activado ahora si se puede ejecutar el script: python3 02-limpieza.py

echo "Iniciando instalación de ambiente ..."

echo "Instalando soporte para entornos virtuales (python3-venv)..."
sudo apt install -y python3-venv

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual 'venv'..."
    python3 -m venv venv
else
    echo "Ya existe un entorno virtual llamado 'venv'."
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Actualizando pip dentro del entorno..."
pip install --upgrade pip

echo "Instalando librerías ETL necesarias..."
pip install pandas sqlalchemy psycopg2-binary

echo "---------------------------------------"
echo "Entorno virtual listo!"
echo "Para activarlo de nuevo se usa: source venv/bin/activate"
echo ""
echo "Con el ambiente activado ya se puede ejecutar:"
echo "    python3 02-limpieza.py"
echo "    python3 03-carga-postgres.py"
echo "---------------------------------------"
