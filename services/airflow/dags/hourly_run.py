from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'abdellah',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'hourly',
    default_args=default_args,
    description='Ingest and transform customer data',
    schedule_interval='*/5 * * * *',
    catchup=False,
)

ingest_task = BashOperator(
    task_id='ingest_customers',
    bash_command='python /opt/airflow/ingest/ingest.py',
    dag=dag,
)

transform_task = BashOperator(
    task_id='transform_customers',
    bash_command='python /opt/airflow/transform/transform.py',
    dag=dag,
)

ingest_task >> transform_task 
