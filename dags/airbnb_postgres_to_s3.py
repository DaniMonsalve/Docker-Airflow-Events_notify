from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import csv
import psycopg2
import numpy as np


#Definir Args:
default_args = {
    "owner": "darshil",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 8),
}

#Definir DAG:
dag = DAG(
    dag_id = "airbnb_postgres_to_s3",
    default_args = default_args,
    description = "ETL data from postgres to S3",
    schedule_interval = timedelta(days=1),
)

Listing_dates = ["2024-06-15","2024-09-11","2024-12-12"]

def download_csv():
    Listing_url_template="https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/{date}/visualisations/listings.csv"
    for date in Listing_dates:
        url = Listing_url_template.format(date=date)
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"/tmp/airbnbdata/listing-{date}.csv", 'wb') as f:
                f.write(response.content)
        else:
            print(f"failed to download {url}")

def preprocess_csv():
    for date in Listing_dates:
        input_file = f'/tmp/airbnbdata/listing-{date}.csv'
        output_file = f'/tmp/airbnbdata/listing-{date}-processed.csv'
        df = pd.read_csv(input_file)
        df.fillna('',inplace=True)
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

def load_csv_to_postgres():
    conn = psycopg2.connect("dbname='postgres' user='airflow' host='postgres' password='airflow'")
    cur = conn.cursor()
    for date in Listing_dates:
        processed_csv = f'/tmp/airbnbdata/listing-{date}-processed.csv'
        with open(processed_csv, 'r') as f:
            cur.copy_expert("COPY listings FROM stdin WITH CSV HEADER QUOTE '\"' ", f)
        conn.commit()
    cur.close()
    conn.close()    

download_csv_task = PythonOperator(
    task_id = "download_csv",
    python_callable = download_csv,
    dag=dag,
)

preprocess_csv_task = PythonOperator(
    task_id = "preprocess_csv",
    python_callable = preprocess_csv,
    dag=dag,
)

create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="airbnb_postgres",
    sql="""
    DROP TABLE IF EXISTS listings;
    CREATE TABLE IF NOT EXISTS listings (
        id BIGINT,
        name TEXT,
        host_id INTEGER,
        host_name VARCHAR(200),
        neighbourhood_group VARCHAR(200),
        neighbourhood VARCHAR(200),
        latitude NUMERIC(18,16),
        longitude NUMERIC(18,16),
        room_type VARCHAR(100),
        price VARCHAR(100),
        minimum_nights INTEGER,
        number_of_reviews INTEGER,
        last_review VARCHAR(200),
        reviews_per_month VARCHAR(200),
        calculated_host_listings_count INTEGER,
        availability_365 INTEGER,
        number_of_reviews_ltm INTEGER,
        license TEXT
    );
    """,
    dag=dag,
)

load_csv_task = PythonOperator(
    task_id = "load_csv_to_postgres",
    python_callable = load_csv_to_postgres,
    dag=dag,
)

download_csv_task >> preprocess_csv_task >> create_table >> load_csv_task