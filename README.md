Diferent workflow-orchestrations using Apache-airflow

## Prerequisites
Before using this pipeline, make sure you have the following installed:

    Docker
    Apache Airflow
    Python 3.x

## Folder Structure
dags/: Contains the Airflow DAG files.

docker-compose.yml: Defines the services for running the Docker containers, including Airflow.

logs/: Contains log files from the DAG runs. (Not included with gitignore)

output/: The directory where downloaded images are saved outside the Docker container, as well other data.


## Download Images Events DAG
Apache Airflow pipeline that automates the process of downloading event data from an external API. It retrieves event information, downloads associated images in binary format, and saves them outside the Docker container, making them accessible from the host system. Finally, the pipeline sends a notification with the count of successfully downloaded images.

<img width="411" alt="graph view" src="https://github.com/user-attachments/assets/ba31f738-cb1b-408b-8e64-409af7ba43b0">

## Features
- Event data retrieval from the Real-Time Events Search API: The pipeline fetches event data, including associated images.

- Image downloading: Images related to the events are downloaded in binary format.

- Data storage: Images are saved outside the Docker container, in a local directory on the host system, ensuring easy access.

- Notification: After the images are successfully downloaded, a notification is generated that shows the total number of images fetched.

## Workflow
API Integration: Event data is retrieved via the "Real-Time Events Search" API.

<img width="956" alt="Api_utilizada" src="https://github.com/user-attachments/assets/dea8b4ab-5e3b-42d3-a60e-8fa9689a472c">


Docker Containers: The pipeline uses docker-compose.yml to spin up the necessary containers (including Airflow).

<img width="946" alt="Docker first run" src="https://github.com/user-attachments/assets/d68e6ff8-b7ff-477d-8129-2e38a153c91a">


Airflow DAG: The Download_events DAG is triggered manually via Airflow to begin the process of downloading event data and images.

<img width="949" alt="Ejecucion del dag" src="https://github.com/user-attachments/assets/31c9ff02-1991-477d-8c4e-81823028cad6">


Local Image Storage: Extracted images are saved locally, outside the Docker container.

<img width="929" alt="imagenes extraidas en binario" src="https://github.com/user-attachments/assets/3ca8862f-c9ac-41dc-b9b5-5100e2cbd969">


Notification: A notification is triggered that indicates how many images were successfully downloaded.

<img width="948" alt="return value" src="https://github.com/user-attachments/assets/db24f200-93be-4cad-af45-7c95836206cf">
<img width="938" alt="downloaded images" src="https://github.com/user-attachments/assets/48c29f47-0f51-43e7-9c0d-9fa8a501b1ba">


## Website events API processing
This DAG processes user events collected from an external API to analyze browsing behavior on an imaginary website. The workflow consists of two main tasks: first, retrieving recent events from the API and storing them in a local JSON file, and then processing this data to calculate daily statistics, such as the number of pages visited per user and the average time spent per visit. These statistics are saved in a CSV file, enabling historical analysis beyond the API's 30-day data retention limit.

<img width="251" alt="2024-12-06 13_13_45-01_unscheduled - Graph - Airflow - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/777c7e04-a5c9-4fb1-a898-47894c0f97c5">

*Check /output/data to see results

<img width="939" alt="2024-12-06 13_13_05-01_unscheduled - Airflow - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/9fbfad71-a1fe-4430-9541-b74d5a80e62b">
