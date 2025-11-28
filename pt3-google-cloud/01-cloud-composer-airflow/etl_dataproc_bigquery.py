from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocStartClusterOperator,
    DataprocSubmitJobOperator,
    DataprocStopClusterOperator,
)
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

cluster_name = 'cluster-incidencia-delictiva'
region = 'us-central1'
project_id = 'ingenieria-de-datos-479016'
bucket_name = 'gs://incidencia-delictiva'
script_path = f'{bucket_name}/etl_spark.py'
temp_bucket = 'dataproc-temp-ingenieria-datos'
dataset = 'inm_estatal_jul25'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    'etl_dataproc_bigquery',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    start = EmptyOperator(task_id='start')

    # Levantar el cluster si estÃ¡ apagado
    start_cluster = DataprocStartClusterOperator(
        task_id="start_cluster",
        project_id=project_id,
        region=region,
        cluster_name=cluster_name,
    )

    run_dataproc_etl = DataprocSubmitJobOperator(
        task_id="run_pyspark_etl",
        region=region,
        project_id=project_id,
        job={
            "placement": {"cluster_name": cluster_name},
            "pyspark_job": {
                "main_python_file_uri": script_path,
                "args": [
                    '--temp_bucket', temp_bucket,
                    '--dataset', dataset
                ]
            }
        }
    )

    # Apagar el cluster cuando termine
    stop_cluster = DataprocStopClusterOperator(
        task_id="stop_cluster",
        project_id=project_id,
        region=region,
        cluster_name=cluster_name,
        trigger_rule="all_done"  # Se ejecuta aunque falle el ETL
    )

    end = EmptyOperator(task_id='end')

    start >> start_cluster >> run_dataproc_etl >> stop_cluster >> end