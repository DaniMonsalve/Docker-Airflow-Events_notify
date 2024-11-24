## SUM UP
This repository contains an Apache Airflow pipeline that automates the process of downloading event data from an external API. It retrieves event information, downloads associated images in binary format, and saves them outside the Docker container, making them accessible from the host system. Finally, the pipeline sends a notification with the count of successfully downloaded images.

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



## Prerequisites
Before using this pipeline, make sure you have the following installed:

    Docker
    Apache Airflow
    Python 3.x

## Folder Structure
dags/: Contains the Airflow DAG file for downloading events and images.

docker-compose.yml: Defines the services for running the Docker containers, including Airflow.

logs/: Contains log files from the DAG runs.

output/: The directory where downloaded images are saved outside the Docker container.


