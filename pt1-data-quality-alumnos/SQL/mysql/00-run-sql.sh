#!/bin/bash
# Para ejecutar debidamente este script, este debe existir en el mismo nivel que los scripts .sql.
# Además también es necesario darle permisos de ejecución con: chmod +x 00-run-sql.sh
# En caso de que se requiera eliminar todo para regresar al estado inicial,
# basta con ejecutar: docker exec -i mysql_db mysql -uroot < "01_DataBaseInit.sql.rollback"


CONTAINER="mysql_db"
MYSQL_USER="root"

echo "Ejecutando scripts SQL dentro del contenedor '$CONTAINER'..."
echo ""

# Recorre todos los .sql en orden alfabético
for file in *.sql; do
    # Si no hay archivos .sql, evitar mensaje de error
    [ -e "$file" ] || continue
    
    echo "Ejecutando: $file"
    docker exec -i $CONTAINER \
        mysql -u"$MYSQL_USER" < "$file"

    if [ $? -ne 0 ]; then
        echo " Error ejecutando '$file'. Deteniendo proceso."
        exit 1
    fi

    echo "Completado: $file"
    echo "-------------------------------------------"
done

echo ""
echo "Todos los scripts fueron ejecutados con éxito."
