from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ======================================
# CONFIGURACIÃ“N PARA GOOGLE CLOUD
# ======================================
PROJECT = "ingenieria-de-datos-479016"
DATASET = "inm_estatal_jul25"
BUCKET = "gs://incidencia-delictiva"
TEMP_BUCKET = "dataproc-temp-ingenieria-datos"    # bucket temporal obligatorio

CSV_FILE = f"{BUCKET}/INM_estatal_jul25.csv"

# Mapeo CSV â†’ Tabla catÃ¡logo
CATALOG_MAP = {
    'entidad': 'ESTADO',
    'bien_juridico_afectado': 'BIEN_AFECTADO',
    'tipo_delito': 'TIPO_DELITO',
    'subtipo_delito': 'SUBTIPO_DELITO',
    'modalidad': 'MODALIDAD'
}

# ======================================
# MAIN ETL
# ======================================
def etl_spark():
    spark = SparkSession.builder \
        .appName("ETL_Delitos_BigQuery") \
        .config(
            "spark.jars",
            "gs://hadoop-lib/bigquery/bigquery-connector-hadoop3-1.2.0.jar"
        ) \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print("SesiÃ³n Spark en Dataproc iniciada.")

    # ==========================================================
    # 1. LECTURA DEL CSV
    # ==========================================================
    print(f"Leyendo archivo CSV: {CSV_FILE}")
    df_raw = spark.read.csv(CSV_FILE, header=True, inferSchema=True)

    print("Inicio de limpieza y reglas de negocio.")

    # ==========================================================
    # (1) Convertir a mayÃºsculas ciertas columnas
    # ==========================================================
    cols_to_upper = [
        'entidad',
        'bien_juridico_afectado',
        'tipo_delito',
        'subtipo_delito',
        'modalidad'
    ]

    for col_name in cols_to_upper:
        if col_name in df_raw.columns:
            df_raw = df_raw.withColumn(col_name, F.upper(F.col(col_name)))
            print(f"{col_name} convertido a mayÃºsculas.")

    # ==========================================================
    # (2) Eliminar columnas innecesarias
    # ==========================================================
    cols_to_drop = ['anio', 'mes', 'entidad federativa']
    cols_drop_existing = [c for c in cols_to_drop if c in df_raw.columns]

    if cols_drop_existing:
        df_raw = df_raw.drop(*cols_drop_existing)
        print(f"Columnas eliminadas: {cols_drop_existing}")

    # ==========================================================
    # (3) TRIM
    # ==========================================================
    print("Aplicando trim a todas las columnas de texto.")
    for col_name, dtype in df_raw.dtypes:
        if dtype == "string":
            df_raw = df_raw.withColumn(col_name, F.trim(F.col(col_name)))

    # ==========================================================
    # (4) Eliminar duplicados
    # ==========================================================
    df_raw = df_raw.dropDuplicates()
    print("Duplicados eliminados.")

    # ----------------------------------------------------------
    # 2. CREACIÃ“N DE CATÃLOGOS
    # ----------------------------------------------------------
    print("ConstrucciÃ³n de catÃ¡logos.")
    catalog_dfs = {}

    for csv_col, catalog_table in CATALOG_MAP.items():
        print(f"Procesando catÃ¡logo {catalog_table} con base en {csv_col}.")

        df_cat = df_raw.select(csv_col).distinct()

        w = Window.orderBy(csv_col)
        df_cat = df_cat.withColumn(
            f"id_{catalog_table.lower()}",
            F.row_number().over(w)
        )

        rename_to = "entidad" if catalog_table == "ESTADO" else "descripcion"
        df_cat = df_cat.withColumnRenamed(csv_col, rename_to)

        catalog_dfs[csv_col] = df_cat

        df_cat.write.format("bigquery") \
            .option("table", f"{PROJECT}:{DATASET}.{catalog_table}") \
            .option("temporaryGcsBucket", TEMP_BUCKET) \
            .mode("overwrite") \
            .save()

        print(f"CatÃ¡logo guardado: {DATASET}.{catalog_table}")

    # ----------------------------------------------------------
    # 3. TABLA PRINCIPAL
    # ----------------------------------------------------------
    print("Construyendo tabla principal.")

    df_main = df_raw

    for csv_col, df_cat in catalog_dfs.items():
        id_col = [c for c in df_cat.columns if c.startswith("id_")][0]
        text_col = "entidad" if "entidad" in df_cat.columns else "descripcion"

        print(f"Haciendo JOIN entre {csv_col} y catÃ¡logo {id_col}.")

        df_main = df_main.join(
            df_cat,
            df_main[csv_col] == df_cat[text_col],
            "left"
        ).drop(csv_col, text_col)

    df_main = df_main.withColumn(
        "fecha_delito",
        F.to_date(F.col("fecha"), "dd/MM/yyyy")
    )

    w_main = Window.orderBy("fecha_delito")
    df_main = df_main.withColumn(
        "id_indice_estatal_delito",
        F.row_number().over(w_main)
    )

    final_cols = [
        "id_indice_estatal_delito",
        "fecha_delito",
        "incidencia_delictiva",
        "id_estado",
        "id_bien_afectado",
        "id_tipo_delito",
        "id_subtipo_delito",
        "id_modalidad"
    ]

    df_final = df_main.select(*final_cols)

    df_final.write.format("bigquery") \
        .option("table", f"{PROJECT}:{DATASET}.INDICE_ESTATAL_DELITO") \
        .option("temporaryGcsBucket", TEMP_BUCKET) \
        .mode("overwrite") \
        .save()

    print("ETL completa. CatÃ¡logos y tabla principal almacenados en BigQuery.")

    spark.stop()


if __name__ == "__main__":
    etl_spark()