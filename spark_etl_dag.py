from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Definir la ruta donde están tus scripts DENTRO del contenedor
WORK_DIR = "/shared_data/pt2-incidencia-delictiva/02-spark"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'incidencia_delictiva_etl',
    default_args=default_args,
    description='Orquestación de scripts Spark para Incidencia Delictiva',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['spark', 'etl', 'docker'],
) as dag:

    # Tarea 1: Configurar entorno
    t1_config = BashOperator(
        task_id='configurar_entorno',
        # 🚨 FIX DEFINITIVO: Usamos sh -c para forzar el tratamiento como comando shell simple
        bash_command=f"sh -c 'exec {WORK_DIR}/config.sh'",
        cwd=WORK_DIR, 
        append_env=True
    )

    # Tarea 2: Limpieza de datos (ETL_1)
    t2_limpieza = BashOperator(
        task_id='limpieza_datos',
        # Aplicar el mismo patrón
        bash_command=f"sh -c 'exec {WORK_DIR}/script_1.sh'",
        cwd=WORK_DIR,
        append_env=True
    )

    # Tarea 3: Carga a Base de Datos (ETL_2)
    t3_carga_bd = BashOperator(
        task_id='carga_base_datos',
        # Aplicar el mismo patrón
        bash_command=f"sh -c 'exec {WORK_DIR}/script_2.sh'",
        cwd=WORK_DIR,
        append_env=True
    )

    t1_config >> t2_limpieza >> t3_carga_bd
