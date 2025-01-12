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

### Features
- Event data retrieval from the Real-Time Events Search API: The pipeline fetches event data, including associated images.

- Image downloading: Images related to the events are downloaded in binary format.

- Data storage: Images are saved outside the Docker container, in a local directory on the host system, ensuring easy access.

- Notification: After the images are successfully downloaded, a notification is generated that shows the total number of images fetched.

### Workflow
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


## Automation of Wikipedia Pageviews Processing
This Airflow workflow aims to automate the process of downloading, extracting, and analyzing Wikipedia pageview data to predict the stock behavior of different companies based on the amount of visits to their pages. Through a set of templated tasks, the workflow periodically downloads the compressed pageview files from a remote server, extracts them, processes, and analyzes the data from selected entities. The analysis results are then stored in a PostgreSQL database for further querying. Additionally, Airflow’s templating techniques are used to dynamically handle dates and other parameters, allowing the workflow to run efficiently and at scale.

Airflow Workflow Diagram

<img width="356" alt="esquema wiki" src="https://github.com/user-attachments/assets/f002e842-8dfa-455b-b7ba-17e15c316c2c" />

Screenshot of the Data Copying Process Inside the Airflow Container

<img width="944" alt="copi data inside airflow container" src="https://github.com/user-attachments/assets/ca2be16d-4dc0-4f0c-b507-9b8731ae8aad" />

Evidence of the Docker PostgreSQL Container Running

<img width="954" alt="docker postgres container" src="https://github.com/user-attachments/assets/372bf590-a0d2-451c-9b92-473312c0da04" />

How to Access the PostgreSQL Database

<img width="869" alt="acceder a postgres database" src="https://github.com/user-attachments/assets/cc0fcf58-b221-40b2-8b49-eafa1d83b821" />

Creation of the Database Used

<img width="466" alt="create database" src="https://github.com/user-attachments/assets/1c9de649-b84b-4d64-ba6c-dbd6ad7ddbe5" />

How the Generated PostgreSQL Query Looks

<img width="734" alt="postgres_query generated" src="https://github.com/user-attachments/assets/4839b48d-5bb9-4806-b164-8d6bfa5bd59c" />


## Trigger Workflow
The workflow in Airflow designed to handle the arrival of supermarket promotion data automates the ingestion of this data by monitoring the appearance of specific files in a shared storage system. Using sensors like FileSensor and PythonSensor, the process detects the presence of data files and the success file (_SUCCESS), which indicates that the data has been fully loaded. The workflow adapts to data delivery delays by employing a timeout and setting the sensor mode to "reschedule," preventing blocking and allowing the system to continue processing tasks without consuming unnecessary resources. This ensures that the workflow operates efficiently and scalably, even when data arrives at unpredictable times.

Workflow Diagram: The implemented workflow is outlined in the attached diagram, illustrating the sequence and logic of tasks from data detection to processing.

<img width="363" alt="2024-12-19 17_15_33-trigger_workflow - Graph - Airflow y 2 páginas más - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/12abe16b-94cf-4cec-b991-d02a486ee9f5" />
<img width="951" alt="2024-12-19 17_02_03-trigger_workflow - Graph - Airflow y 2 páginas más - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/f5702526-798b-486b-9c73-b92694088b07" />


Data Detection Evidence: Screenshots demonstrate the successful detection of available data files and the triggering of subsequent tasks, showcasing the integration of sensors.

<img width="939" alt="2024-12-19 17_07_28-trigger_workflow - Airflow y 2 páginas más - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/a5631a9e-479b-4912-bfb3-b408cb3a28e6" />

Timeout Failure Evidence: Evidence of the timeout mechanism functioning correctly is provided, including logs or visual indicators showing how the system identifies delays and appropriately fails tasks when the timeout is exceeded.

<img width="832" alt="2024-12-19 17_11_38-trigger_workflow - Airflow y 2 páginas más - Perfil 1_ Microsoft​ Edge" src="https://github.com/user-attachments/assets/0790596e-2dc2-4d00-87a7-b959cc1cfaaf" />
