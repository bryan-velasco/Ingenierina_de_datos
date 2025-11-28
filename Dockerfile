# Usamos la versión 2.10.5 para que coincida con lo que tu sistema intenta descargar
FROM apache/airflow:2.10.5

# Pasamos a usuario root para instalar paquetes del sistema operativo
USER root

# 1. Instalar OpenJDK 17 (Java), curl y herramientas básicas
# (Java 17 es la recomendada para versiones modernas de Airflow y Spark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk procps ant curl && \
    apt-get clean;

# 2. Configurar variable de entorno JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME

# 3. Descargar e Instalar los binarios de Apache Spark
# Esto es OBLIGATORIO para tener el comando 'spark-submit' dentro del contenedor
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
RUN curl -o spark.tgz https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xf spark.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark.tgz

# 4. Configurar variables de entorno de Spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# 5. Volver al usuario airflow para instalar librerías de Python
USER airflow

# 6. Instalar librerías de Python y CORREGIR el error de OpenLineage
# La opción --no-cache-dir ayuda a mantener la imagen ligera
RUN pip install --no-cache-dir \
    "apache-airflow-providers-apache-spark" \
    "pyspark==3.5.1" \
    "apache-airflow-providers-openlineage>=1.8.0"
