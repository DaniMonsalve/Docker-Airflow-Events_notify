## SUM UP
This repository contains an Apache Airflow pipeline that automates the process of downloading event data from an external API. It retrieves event information, downloads associated images in binary format, and saves them outside the Docker container, making them accessible from the host system. Finally, the pipeline sends a notification with the count of successfully downloaded images.

## Features
- Event data retrieval from the Real-Time Events Search API: The pipeline fetches event data, including associated images.

- Image downloading: Images related to the events are downloaded in binary format.

- Data storage: Images are saved outside the Docker container, in a local directory on the host system, ensuring easy access.

- Notification: After the images are successfully downloaded, a notification is generated that shows the total number of images fetched.

## Workflow
API Integration: Event data is retrieved via the "Real-Time Events Search" API.


Docker Containers: The pipeline uses docker-compose.yml to spin up the necessary containers (including Airflow).


Airflow DAG: The Download_events DAG is triggered manually via Airflow to begin the process of downloading event data and images.


Local Image Storage: Extracted images are saved locally, outside the Docker container.


Notification: A notification is triggered that indicates how many images were successfully downloaded.



## Prerequisites
Before using this pipeline, make sure you have the following installed:

    Docker
    Docker Compose
    Apache Airflow
    Python 3.x
    Setup Instructions

## Folder Structure
dags/: Contains the Airflow DAG file for downloading events and images.
docker-compose.yml: Defines the services for running the Docker containers, including Airflow.
logs/: Contains log files from the DAG runs.
output/: The directory where downloaded images are saved outside the Docker container.
License

