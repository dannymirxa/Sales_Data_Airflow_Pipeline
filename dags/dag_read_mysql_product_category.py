from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import sys

sys.path.append('/opt/airflow/operation')

#import module from operation folder
from read_mysql_product_category import main
from upload_file_to_drive_product_category import upload_excel

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

# Set the DAG scheduler
dag = DAG(
    'mysql_product_category_report',
    default_args=default_args,
    description='Generate product category report from MySQL every month',
    schedule_interval='59 23 28-31 * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['mysql', 'report'],
)

# Define the tasks

## Create the Excel file
generate_report = PythonOperator(
    task_id='generate_product_category_report',
    python_callable=main,
    dag=dag,
)

def upload_file_wrapper():
    return upload_excel('/opt/airflow/file_output/product_category.xlsx')

## Upload the Excel file to Google Drive
upload_file = PythonOperator(
    task_id='upload_product_category_report_to_drive',
    python_callable=upload_file_wrapper,
    dag=dag,
)

# Sends email to recipients if upload_file task is successful
send_success_email = EmailOperator(
    task_id='send_success_email',
    to=['danialmirxa96@gmail.com', 'william.cheah@mrdiy.com' , 'andrew.pung@mrdiy.com'],
    subject='Product Category Report Task Success',
    html_content="""
        <h3>Task Completed Successfully</h3>
        <p>Product Category Report has completed successfully.</p>
        <p>Execution date: {{ ds }}</p>
    """,
    dag=dag,
)

# Set task dependencies
generate_report >> upload_file >> send_success_email