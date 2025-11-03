import os
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataTransferJsonAvro") \
    .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.5.1") \
    .getOrCreate()
print("--- Leyendo el archivo CSV ---")
df = spark.read.csv("INM_estatal_jul25.csv", header=True, inferSchema=True)

df.show(5)

# 1. Parquet
print("\n--- Guardando el DataFrame como Parquet ---")
df.coalesce(1).write.mode("overwrite").parquet("INM_estatal_jul25.parquet")
print("Archivo Parquet guardado.")

print("\n--- Leyendo el archivo Parquet ---")
df_parquet = spark.read.parquet("INM_estatal_jul25.parquet")

df_parquet.show(5)

df_parquet.printSchema()

# 2. TXT
print("\n--- Guardando el DataFrame como TXT ---")
df.write.mode("overwrite").option("sep", " ").csv("INM_estatal_jul25_txt")
print("Archivo TXT guardado.")

print("\n--- Leyendo el archivo TXT ---")
df_txt = spark.read.text("INM_estatal_jul25_txt")

df_txt.show(5, truncate=False)

#3 JSON
print("\n--- Guardando el DataFrame como JSON ---")
df.write.mode("overwrite").json("INM_estatal_jul25.json")
print("Archivo JSON guardado.")

print("\n--- Leyendo el archivo JSON ---")
df_json = spark.read.json("INM_estatal_jul25.json")
df_json.show(5)
df_json.printSchema()

# 4. Avro
print("\n--- Guardando el DataFrame como Avro ---")
# La librería de Avro se carga automáticamente gracias a la configuración de Spark.
df.write.mode("overwrite").format("avro").save("INM_estatal_jul25.avro")
print("Archivo Avro guardado.")

print("\n--- Leyendo el archivo Avro ---")
df_avro = spark.read.format("avro").load("INM_estatal_jul25.avro")
df_avro.show(5)
df_avro.printSchema()

spark.stop()
