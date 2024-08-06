from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import sqlite3
import os

# Define the directory to use for saving files
etl_dir = os.path.dirname(os.path.abspath(__file__))
etl_project_dir = os.path.join(etl_dir, 'etl_project')
os.makedirs(etl_project_dir, exist_ok=True)

# Step 1: Extract
def extract_data():
    api_url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(etl_project_dir, 'extracted_data.csv'), index=False)
    print("Data extracted successfully.")

# Step 2: Transform
def transform_data():
    df = pd.read_csv(os.path.join(etl_project_dir, 'extracted_data.csv'))
    df['id'] = df['id'].astype(str)
    df.to_csv(os.path.join(etl_project_dir, 'transformed_data.csv'), index=False)
    print("Data transformed successfully.")

# Step 3: Load
def load_data():
    df = pd.read_csv(os.path.join(etl_project_dir, 'transformed_data.csv'))
    db_path = os.path.join(etl_project_dir, 'etl_database.db')
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql('api_data', con=conn, if_exists='replace', index=False)
        print("Data loaded successfully into the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='A simple ETL DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False  # Optional: To avoid backfilling DAG runs
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
