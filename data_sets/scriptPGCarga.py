import csv
import json
import pandas as pd
import psycopg2          # 👈 este es el que falta
from fastavro import reader as avro_reader


# ---- CONFIGURACIÓN DE LA BASE DE DATOS ----
db_config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'delitos_db',
    'user': 'usuario_simple',
    'password': 'password123'
}

# Archivo de entrada
data_file_path = '1.parquet'


# ---- Mapeo de columnas del dataset a las tablas de la BD ----
catalog_map = {
    'entidad': ('ESTADO', 'id_estado', 'entidad'),
    'bien_juridico_afectado': ('BIEN_AFECTADO', 'id_bien_afectado', 'descripcion'),
    'tipo_delito': ('TIPO_DELITO', 'id_tipo_delito', 'descripcion'),
    'subtipo_delito': ('SUBTIPO_DELITO', 'id_subtipo_delito', 'descripcion'),
    'modalidad': ('MODALIDAD', 'id_modalidad', 'descripcion')
}

def load_dataset(file_path):
    """Devuelve un generador de filas (diccionarios) desde CSV, Avro, JSON o Parquet."""
    if file_path.endswith(".csv"):
        with open(file_path, 'r', encoding='utf-8') as f:
            yield from csv.DictReader(f)

    elif file_path.endswith(".avro"):
        with open(file_path, 'rb') as f:
            for record in avro_reader(f):
                yield record

    elif file_path.endswith(".json"):
        with open(file_path, 'r', encoding='utf-8') as f:
            first_char = f.read(1)
            f.seek(0)  # volver al inicio del archivo

            if first_char == '[':  # JSON tipo array
                data = json.load(f)
                for row in data:
                    yield row
            else:  # JSON tipo JSONL / NDJSON (un objeto por línea)
                for line in f:
                    if line.strip():  # ignora líneas vacías
                        yield json.loads(line)


    elif file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)
        for _, row in df.iterrows():
            yield row.to_dict()

    else:
        raise ValueError("Formato de archivo no soportado (usa .csv, .avro, .json o .parquet)")



def load_data():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        catalogs = {col: {} for col in catalog_map.keys()}
        next_id = {col: 1 for col in catalog_map.keys()}

        # ---- FASE 1: PROCESAR CATÁLOGOS ----
        print("Fase 1: Procesando catálogos...")
        for row in load_dataset(data_file_path):
            for csv_col in catalog_map.keys():
                value = row[csv_col]
                if value not in catalogs[csv_col]:
                    catalogs[csv_col][value] = next_id[csv_col]
                    next_id[csv_col] += 1

        # Limpiar tablas dependientes primero
        cursor.execute("TRUNCATE TABLE INDICE_ESTATAL_DELITO CASCADE;")
        for csv_col, (db_table, _, _) in catalog_map.items():
            cursor.execute(f"TRUNCATE TABLE {db_table} CASCADE;")

        # Insertar catálogos
        for csv_col, (db_table, db_id_col, db_desc_col) in catalog_map.items():
            print(f"Insertando datos en la tabla '{db_table}'...")
            insert_query = f"INSERT INTO {db_table} ({db_id_col}, {db_desc_col}) VALUES (%s, %s)"
            data_to_insert = [(id_val, value) for value, id_val in catalogs[csv_col].items()]
            cursor.executemany(insert_query, data_to_insert)

        # ---- FASE 2: PROCESAR DATOS PRINCIPALES ----
        print("\nFase 2: Insertando datos en la tabla 'INDICE_ESTATAL_DELITO'...")
        
        main_data = []
        for i, row in enumerate(load_dataset(data_file_path)):
            id_estado = catalogs['entidad'][row['entidad']]
            id_bien_afectado = catalogs['bien_juridico_afectado'][row['bien_juridico_afectado']]
            id_tipo_delito = catalogs['tipo_delito'][row['tipo_delito']]
            id_subtipo_delito = catalogs['subtipo_delito'][row['subtipo_delito']]
            id_modalidad = catalogs['modalidad'][row['modalidad']]

            # Convertir fecha dd/mm/yyyy → yyyy-mm-dd
            fecha_parts = row['fecha'].split('/')
            fecha_pg = f"{fecha_parts[2]}-{fecha_parts[1]}-{fecha_parts[0]}"

            main_data.append((
                i + 1,
                fecha_pg,
                int(row['incidencia_delictiva']),
                id_estado,
                id_bien_afectado,
                id_tipo_delito,
                id_subtipo_delito,
                id_modalidad
            ))

        main_insert_query = """
        INSERT INTO INDICE_ESTATAL_DELITO (
            id_indice_estatal_delito, fecha_delito, incidencia_delictiva, 
            id_estado, id_bien_afectado, id_tipo_delito, 
            id_subtipo_delito, id_modalidad
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(main_insert_query, main_data)

        conn.commit()
        print("\nCarga de datos completada exitosamente en PostgreSQL. 🎉")

    except psycopg2.Error as err:
        print(f"Error de PostgreSQL: {err}")
    except FileNotFoundError:
        print(f"Error: El archivo '{data_file_path}' no se encontró.")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    load_data()
