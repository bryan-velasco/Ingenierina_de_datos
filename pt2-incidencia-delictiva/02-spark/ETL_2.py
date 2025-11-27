import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BASE_PATH = '/shared_data/pt2-incidencia-delictiva/02-spark/' 
JAR_NAME = 'postgresql-42.7.3.jar'

# Configuración
INPUT_CLEAN_FILE = 'dataset_modificado' # Leemos la carpeta generada antes

DB_CONFIG = {
    "url": "jdbc:postgresql://postgresql:5432/incidencias_spark",
    "user": "admin",      
    "password": "admin123", 
    "driver": "org.postgresql.Driver"
}

CATALOG_MAP = {
    'entidad': 'estado',
    'bien_juridico_afectado': 'bien_afectado',
    'tipo_delito': 'tipo_delito',
    'subtipo_delito': 'subtipo_delito',
    'modalidad': 'modalidad'
}

def execute_jdbc_statement(spark, sql_query):
    """Ejecuta SQL directo (TRUNCATE, DROP, etc)"""
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

def upload_process():
    # Construye la ruta completa al driver
    DRIVER_PATH = BASE_PATH + JAR_NAME

    spark = SparkSession.builder \
        .appName("ETL_Paso2_Carga") \
        .config("spark.driver.extraClassPath", DRIVER_PATH) \
        .config("spark.executor.extraClassPath", DRIVER_PATH) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    try:
        print(f"Leyendo datos transformados de {INPUT_CLEAN_FILE}")
        df_clean = spark.read.csv(INPUT_CLEAN_FILE, header=True, inferSchema=True)

        #Limpieza de tablas en BD 
        tables_to_truncate = ["indice_estatal_delito"] + list(CATALOG_MAP.values())
        tables_str = ", ".join(tables_to_truncate)
        
        print("Limpiando tablas")
        execute_jdbc_statement(spark, f"TRUNCATE TABLE {tables_str} CASCADE;")

        # Procesamiento de Catálogos
        catalog_dfs = {}
        
        for csv_col, db_table in CATALOG_MAP.items():
            print(f"Cargando catálogo: {db_table}")
            
            # Generar IDs únicos basados en el CSV limpio
            df_cat = df_clean.select(csv_col).distinct()
            window_spec = Window.orderBy(csv_col)
            
            # Crear ID numérico
            df_cat = df_cat.withColumn(f"id_{db_table.lower()}", F.row_number().over(window_spec))
            
            # Se eliminó la lógica especial
            target_col_name = "descripcion" 
            df_cat = df_cat.withColumnRenamed(csv_col, target_col_name)
            
            # Guardar referencia en memoria para el Join posterior
            catalog_dfs[csv_col] = df_cat.withColumnRenamed(target_col_name, csv_col)
            
            # Insertar Catálogo en BD
            df_to_db = df_cat
            df_to_db.write.format("jdbc") \
                .options(**DB_CONFIG) \
                .option("dbtable", db_table) \
                .mode("append") \
                .save()

        #Procesamiento Tabla de Hechos
        print("Construyendo tabla de hechos...")
        df_main = df_clean

        # Joins para reemplazar textos por IDs
        for csv_col, df_cat_with_id in catalog_dfs.items():
            # Identificar nombre columna ID
            id_col = [c for c in df_cat_with_id.columns if c.startswith("id_")][0]
            
            df_main = df_main.join(
                df_cat_with_id,
                on=csv_col, #Join por el texto
                how="left"
            ).drop(csv_col) #Tiramos el texto, nos quedamos el ID

        # Generar ID primario para la tabla de hechos
        w_main = Window.orderBy("fecha_delito")
        df_main = df_main.withColumn("id_indice_estatal_delito", F.row_number().over(w_main))
        
        # Selección final de columnas
        final_cols = [
            "id_indice_estatal_delito", "fecha_delito", "incidencia_delictiva",
            "id_estado", "id_bien_afectado", "id_tipo_delito", 
            "id_subtipo_delito", "id_modalidad"
        ]
        
        df_final = df_main.select(*final_cols)

        print("Insertando hechos en indice_estatal_delito...")
        df_final.write.format("jdbc") \
            .options(**DB_CONFIG) \
            .option("dbtable", "indice_estatal_delito") \
            .mode("append") \
            .save()

        print("Carga finalizada correctamente.")

    except Exception as e:
        print(f"Fallo en la carga: {e}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    upload_process()
