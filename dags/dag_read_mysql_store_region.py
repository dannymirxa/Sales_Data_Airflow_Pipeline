from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add the operations directory to Python path
# dag_folder = os.path.dirname(os.path.abspath(__file__))
# operations_folder = os.path.join(os.path.dirname(dag_folder), 'operation')
# sys.path.append(operations_folder)

import sys
sys.path.append('/opt/airflow/operation')

from read_mysql_store_region import main

# Import the main function from your script
# from operation.read_mysql_store_region import main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_store_region_report',
    default_args=default_args,
    description='Generate store region report from MySQL every Wednesday',
    schedule_interval='0 15 * * 3',  # Every Wednesday at 3 PM (15:00)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mysql', 'report'],
)

# Define the task
generate_report = PythonOperator(
    task_id='generate_store_region_report',
    python_callable=main,
    dag=dag,
)

# Set task dependencies (in this case, we only have one task)
generate_report