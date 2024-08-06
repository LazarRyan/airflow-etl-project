import pandas as pd
import requests
import sqlite3
import os

# Define the directory to use for saving files
etl_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the etl_project directory exists
etl_project_dir = os.path.join(etl_dir, 'etl_project')
os.makedirs(etl_project_dir, exist_ok=True)

# Step 1: Extract
def extract_data(api_url):
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(etl_project_dir, 'extracted_data.csv'), index=False)

# Step 2: Transform
def transform_data():
    df = pd.read_csv(os.path.join(etl_project_dir, 'extracted_data.csv'))
    df['id'] = df['id'].astype(str)
    df.to_csv(os.path.join(etl_project_dir, 'transformed_data.csv'), index=False)

# Step 3: Load
def load_data():
    df = pd.read_csv(os.path.join(etl_project_dir, 'transformed_data.csv'))
    db_path = os.path.join(etl_project_dir, 'etl_database.db')
    
    # Use sqlite3 connection directly
    conn = sqlite3.connect(db_path)
    
    try:
        df.to_sql('api_data', con=conn, if_exists='replace', index=False)
        print("Data loaded successfully into the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Main ETL function
def etl_process():
    api_url = 'https://jsonplaceholder.typicode.com/users'
    
    # Extract
    extract_data(api_url)
    print("Data extracted successfully.")
    
    # Transform
    transform_data()
    print("Data transformed successfully.")
    
    # Load
    load_data()

# Run the ETL process
if __name__ == '__main__':
    etl_process()
