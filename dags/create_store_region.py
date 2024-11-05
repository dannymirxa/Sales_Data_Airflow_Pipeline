from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

def my_sql_engine():
    return create_engine('mysql+pymysql://myuser:mypassword@localhost:3306/diy')

def create_table(table: str) -> pd.DataFrame:
    query = f'''
    SELECT {table}, 
           SUM(sales_qty) as sales_qty, 
           SUM(sales_qty*price) as sales_amount,
           SUM(sales_qty*cost) as sales_cost,
           SUM((sales_qty*price) - (sales_qty*cost)) as profit
    FROM Sales sl 
    INNER JOIN Products p ON sl.product_code = p.product_code
    INNER JOIN Store st ON sl.store_code = st.store_code
    GROUP BY {table};
    '''
    with my_sql_engine().connect() as conn:
        return pd.read_sql_query(query, conn.connection)

def set_column_width(sheet, widths):
    for col, width in widths.items():
        sheet.column_dimensions[col].width = width

def save_to_excel(dataframes, filename, column_widths):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            set_column_width(writer.sheets[sheet_name], column_widths)

def main():
    dataframes = {
        'store_region': create_table('store_region')
    }
    column_widths = {'A': 20, 'B': 15, 'C': 15, 'D': 15, 'E': 15}
    save_to_excel(dataframes, 'store_region.xlsx', column_widths)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 5),
    'retries': 1,
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
)

task1 = PythonOperator(
    task_id='create_table',
    python_callable=create_table,
    op_args=['store_region'],
    dag=dag,
)

task2 = PythonOperator(
    task_id='save_to_excel',
    python_callable=save_to_excel,
    op_args=[{'store_region': create_table('store_region')}, 'store_region.xlsx', {'A': 20, 'B': 15, 'C': 15, 'D': 15, 'E': 15}],
    dag=dag,
)

task1 >> task2
