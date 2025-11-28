from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'proyectoingdatos',
    'start_date': datetime(2025, 11, 25),
    'retries': 0,
}

with DAG('etl_completo_incidencia',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    # Variables de ruta
    base_path = "/shared_data/pt2-incidencia-delictiva/02-spark"
    jars = "/shared_data/drivers/postgresql-42.7.8.jar"

    # Tarea 1: Limpieza
    clean_task = BashOperator(
        task_id='etl_paso1_limpieza',
        bash_command=f"""
        spark-submit --master local[*] \
        {base_path}/ETL_1.py
        """
    )

    # Tarea 2: Carga (Necesita el JAR del driver)
    load_task = BashOperator(
        task_id='etl_paso2_carga_bd',
        bash_command=f"""
        spark-submit --master local[*] \
        --jars {jars} \
        --driver-class-path {jars} \
        {base_path}/ETL_2.py
        """
    )

    # Definir dependencia: Primero limpia, luego carga
    clean_task >> load_task
