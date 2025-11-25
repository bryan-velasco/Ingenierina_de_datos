import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Configuración de conexión
DB_CONFIG = {
    "url": "jdbc:postgresql://localhost:5432/incidencias_spark",
    "user": "usuario",
    "password": "usuario",
    "driver": "org.postgresql.Driver"
}

CSV_FILE = 'INM_estatal_jul25.csv'

# Mapeo: Columna CSV -> Tabla Base de Datos
CATALOG_MAP = {
    'entidad': 'ESTADO',
    'bien_juridico_afectado': 'BIEN_AFECTADO',
    'tipo_delito': 'TIPO_DELITO',
    'subtipo_delito': 'SUBTIPO_DELITO',
    'modalidad': 'MODALIDAD'
}

def execute_jdbc_statement(spark, sql_query):
    """Ejecuta una sentencia SQL directa usando el driver JDBC del contexto."""
    try:
        driver_manager = spark._sc._gateway.jvm.java.sql.DriverManager
        con = driver_manager.getConnection(
            DB_CONFIG["url"], DB_CONFIG["user"], DB_CONFIG["password"]
        )
        stmt = con.createStatement()
        stmt.execute(sql_query)
        stmt.close()
        con.close()
        print(f"SQL ejecutado: {sql_query}")
    except Exception as e:
        print(f"Error ejecutando SQL: {e}")
        raise e

def etl_process():
    spark = SparkSession.builder \
        .appName("ETL_Delitos_Postgres") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. Ingesta
        print(f"Leyendo archivo: {CSV_FILE}")
        df_raw = spark.read.csv(CSV_FILE, header=True, inferSchema=True)

        # 2. Normalización de datos
        cols_to_upper = [
            'entidad', 
            'bien_juridico_afectado', 
            'tipo_delito', 
            'subtipo_delito', 
            'modalidad'
        ]

        # Estandarizar textos a mayúsculas
        for col_name in cols_to_upper:
            if col_name in df_raw.columns:
                df_raw = df_raw.withColumn(col_name, F.upper(F.col(col_name)))

        # Eliminar columnas innecesarias
        cols_to_drop = ['anio', 'mes', 'entidad federativa'] 
        existing_drop_cols = [c for c in cols_to_drop if c in df_raw.columns]
        
        if existing_drop_cols:
            df_raw = df_raw.drop(*existing_drop_cols)

        # 3. Limpieza de tablas (Truncate)
        tables_to_truncate = ["INDICE_ESTATAL_DELITO"] + list(CATALOG_MAP.values())
        tables_str = ", ".join(tables_to_truncate)
        
        truncate_query = f"TRUNCATE TABLE {tables_str} CASCADE;"
        execute_jdbc_statement(spark, truncate_query)

        # 4. Procesamiento de Catálogos
        catalog_dfs = {}
        
        for csv_col, db_table in CATALOG_MAP.items():
            print(f"Procesando catálogo: {db_table}")
            
            # Generar IDs únicos
            df_cat = df_raw.select(csv_col).distinct()
            window_spec = Window.orderBy(csv_col)
            
            df_cat = df_cat.withColumn(f"id_{db_table.lower()}", F.row_number().over(window_spec))
            
            # Renombrar columna para coincidir con DB
            target_col_name = "entidad" if db_table == "ESTADO" else "descripcion"
            df_cat = df_cat.withColumnRenamed(csv_col, target_col_name)
            
            catalog_dfs[csv_col] = df_cat
            
            # Carga a DB
            df_cat.write.format("jdbc") \
                .options(**DB_CONFIG) \
                .option("dbtable", db_table) \
                .mode("append") \
                .save()

        # 5. Procesamiento Tabla de Hechos (Principal)
        print("Procesando tabla de hechos")
        df_main = df_raw

        # Joins con catálogos para obtener IDs
        for csv_col, df_cat in catalog_dfs.items():
            id_col = [c for c in df_cat.columns if c.startswith("id_")][0]
            text_col = "entidad" if "entidad" in df_cat.columns else "descripcion"
            
            df_main = df_main.join(
                df_cat,
                df_main[csv_col] == df_cat[text_col],
                "left"
            ).drop(csv_col, text_col)

        # Formato de fecha y generación de ID primario
        df_main = df_main.withColumn("fecha_delito", F.to_date(F.col("fecha"), "dd/MM/yyyy"))
        
        w_main = Window.orderBy("fecha_delito")
        df_main = df_main.withColumn("id_indice_estatal_delito", F.row_number().over(w_main))
        
        final_cols = [
            "id_indice_estatal_delito", "fecha_delito", "incidencia_delictiva",
            "id_estado", "id_bien_afectado", "id_tipo_delito", 
            "id_subtipo_delito", "id_modalidad"
        ]
        
        df_final = df_main.select(*final_cols)

        print("Insertando en INDICE_ESTATAL_DELITO")
        df_final.write.format("jdbc") \
            .options(**DB_CONFIG) \
            .option("dbtable", "INDICE_ESTATAL_DELITO") \
            .mode("append") \
            .save()

        print("Proceso ETL finalizado correctamente.")

    except Exception as e:
        print(f"Fallo en el proceso ETL: {e}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    etl_process()
