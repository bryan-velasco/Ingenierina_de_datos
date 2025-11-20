#!/bin/bash
# Este script debe ejecutarse al mismo nivel donde se tenga el script 01 de creación de tablas

echo "Inicializando BD data_quality de PostgreSQL en Docker..."

CONTAINER="postgresql_db"
SQL_FILE="01-create-tables-postgres.sql"
SQL_IN_CONTAINER="/tmp/01-create-tables.sql"

echo "Copiando archivo SQL al contenedor..."
docker cp "$SQL_FILE" "$CONTAINER:$SQL_IN_CONTAINER"

echo "Ejecutando script SQL dentro del contenedor..."
docker exec -it $CONTAINER psql -U admin -f "$SQL_IN_CONTAINER"

echo "Mostrando tablas creadas..."
docker exec -it $CONTAINER psql -U admin -d data_quality -c "\dt"

echo "BD data_quality inicializada..."