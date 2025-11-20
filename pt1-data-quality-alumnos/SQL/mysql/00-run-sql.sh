#!/bin/bash

# Nombre del contenedor con MySQL
CONTAINER="mysql_db"

# Usuario y contraseña definidos para el MySQL
MYSQL_USER="sys"
MYSQL_PASS="admin123"

echo "Ejecutando scripts SQL dentro del contenedor '$CONTAINER'..."
echo ""

# Recorre todos los .sql en orden alfabético
for file in *.sql; do
    # Si no hay archivos .sql, evitar mensaje de error
    [ -e "$file" ] || continue
    
    echo "Ejecutando: $file"

    docker exec -i $CONTAINER \
        mysql -u"$MYSQL_USER" -p"$MYSQL_PASS" < "$file"

    if [ $? -ne 0 ]; then
        echo " Error ejecutando '$file'. Deteniendo proceso."
        exit 1
    fi

    echo "Completado: $file"
    echo "-------------------------------------------"
done

echo ""
echo "Todos los scripts fueron ejecutados con éxito."
