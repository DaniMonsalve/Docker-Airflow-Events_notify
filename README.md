# Docker-Airflow-Events_notify
This Apache Airflow pipeline automates downloading event data from an external API. It retrieves events, downloads associated images in binary format, and saves them outside the Docker container, making them accessible from the host. Finally, it sends a notification with the count of successfully downloaded images.
