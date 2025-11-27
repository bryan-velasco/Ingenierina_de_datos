import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Archivos
INPUT_FILE = 'INM_estatal_jul25.csv'
OUTPUT_FILE = 'dataset_modificado'

def clean_process():
    spark = SparkSession.builder \
        .appName("ETL_Paso1_Limpieza") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    try:
        print(f"--- PASO 1: Leyendo {INPUT_FILE} ---")
        df = spark.read.csv(INPUT_FILE, header=True, inferSchema=True)

        # Mayúsculas
        cols_to_upper = [
            'entidad', 'bien_juridico_afectado', 
            'tipo_delito', 'subtipo_delito', 'modalidad'
        ]

        for col_name in cols_to_upper:
            if col_name in df.columns:
                df = df.withColumn(col_name, F.upper(F.col(col_name)))

        # Eliminar columnas innecesarias
        cols_to_drop = ['anio', 'mes', 'entidad federativa'] 
        existing_drop_cols = [c for c in cols_to_drop if c in df.columns]
        
        if existing_drop_cols:
            df = df.drop(*existing_drop_cols)

        # Formato de fecha 
        if "fecha" in df.columns:
            df = df.withColumn("fecha_delito", F.to_date(F.col("fecha"), "dd/MM/yyyy"))

        print(f"Guardando datos limpios en: {OUTPUT_FILE}")
        # Guardamos con header para que el siguiente script entienda el esquema
        df.write.mode("overwrite").option("header", "true").csv(OUTPUT_FILE)
        
        print("Limpieza finalizada con éxito.")

    except Exception as e:
        print(f"Error en limpieza: {e}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    clean_process()