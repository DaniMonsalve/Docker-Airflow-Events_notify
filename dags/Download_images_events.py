import json
import pathlib
import requests
from requests.exceptions import MissingSchema, ConnectionError  # Importar excepciones correctamente
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

# Load JSON config file with api keys
with open('/opt/airflow/dags/config_api.json', 'r') as config_file:
    api_host_key = json.load(config_file)

now = datetime.now()
dt_now_string = now.strftime("%d%m%Y%H%M%S")

dag = DAG(
    dag_id="download_events", 
    start_date=days_ago(14),
    schedule_interval=None,
)

download_events = BashOperator(
    task_id="download_events",
    bash_command=(
        f'curl -X GET "https://real-time-events-search.p.rapidapi.com/search-events?query=Concerts%20in%20San-Francisco&date=any&is_virtual=false&start=0" '
        f'-H "X-RapidAPI-Host: {api_host_key["x-rapidapi-host"]}" '
        f'-H "X-RapidAPI-Key: {api_host_key["x-rapidapi-key"]}" '
        f'> /tmp/events_data.json'
    ),
    dag=dag,
)

def _get_pictures():
    # Create the directory for images if it doesn't exist
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # Load events from JSON file
    with open("/tmp/events_data.json") as f:
        events = json.load(f)
        image_urls = [event["thumbnail"] for event in events.get("data", []) if "thumbnail" in event]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except ConnectionError:
                print(f"Could not connect to {image_url}.")

get_pictures = PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,
    dag=dag,
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag,
)

download_events >> get_pictures >> notify
