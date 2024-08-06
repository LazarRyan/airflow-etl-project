### Summary

This `README.md` provides a comprehensive overview of the project, including the setup, structure, usage, and the ETL process defined in the `etl_dag.py` file. It ensures that anyone who wants to understand or use the project has clear and detailed instructions to follow.

# Airflow ETL Project

This project demonstrates an ETL (Extract, Transform, Load) process using Apache Airflow. The process includes extracting data from an API, transforming the data, and loading it into a SQLite database.

## Setup

### Prerequisites

- Python 3.6 or higher
- Apache Airflow
- pandas
- requests
- sqlalchemy

### Installation

### Clone the repository:
bash

git clone https://github.com/yourusername/airflow-etl-project.git

cd airflow-etl-project

### Create and activate a virtual environment:
bash

python3 -m venv airflow_env

source airflow_env/bin/activate

### Install the dependencies:
bash

pip install -r requirements.txt

### Set the AIRFLOW_HOME environment variable:
bash

export AIRFLOW_HOME=$(pwd)/airflow

## Initialize the Airflow database:
bash

airflow db init

## Start the Airflow scheduler and web server:
bash

airflow scheduler &
airflow webserver --port 8080

### Access the Airflow web UI:

Open your browser and go to http://localhost:8080.

# ETL Process
The ETL process is defined in the etl_dag.py file located in the dags directory. It consists of three main tasks:

Extract: Fetch data from an API and save it as a CSV file.

Transform: Read the extracted data, perform transformations, and save the transformed data.

Load: Load the transformed data into an SQLite database.

# DAG File: etl_dag.py

python

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
    
    'email_on_failure': 'your_email@example.com',
    
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

Usage

# Trigger the DAG manually:

In the Airflow web UI, go to the DAGs page, find etl_dag, and click the "Trigger DAG" button.

# Monitor the DAG run:

Monitor the progress and logs of each task in the Airflow web UI.

# Contributing

If you would like to contribute to this project, please open a pull request or issue on GitHub.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

