import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from urllib.request import urlretrieve

dag = DAG(
    dag_id="wikimedia_templating",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
    template_searchpath="/tmp"
)

# Fetch data function
def _get_data(year, month, day, hour, output_path):
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{(int(hour)-5) % 24:0>2}0000.gz"
    )
    urlretrieve(url, output_path)

# Task to download the data
get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wiki/wikipageviews.gz"
    },
    dag=dag,
)

# Task to extract .gz file
extract_gz = BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wiki/wikipageviews.gz",
    dag=dag,
)

# Fetch the pageview counts and write the SQL
def _fetch_pageviews(pagenames, execution_date, ti):
    result = dict.fromkeys(pagenames, 0)
    try:
        # Open and process the data file
        with open("/tmp/wiki/wikipageviews", 'r') as f:
            for line in f:
                try:
                    domain_code, page_title, view_counts, _ = line.split(" ")
                    if domain_code == "en" and page_title in pagenames:
                        result[page_title] = int(view_counts)
                except ValueError as e:
                    print(f"Error processing the line: '{line}'. Error: {e}")
                    continue  # Continue with the next line in case of error

        # Write SQL file
        sql_path = "/tmp/postgres_query.sql"
        with open(sql_path, 'w') as f:
            for pagename, pageviewcount in result.items():
                try:
                    f.write(
                        f"INSERT INTO pageview_counts VALUES ('{pagename}', {pageviewcount}, '{execution_date}');\n"
                    )
                except IOError as e:
                    print(f"Error writing to postgres: {e}")
                    raise

        # Push the SQL file content to XCom so the next task can access it
        with open(sql_path, 'r') as file:
            sql_content = file.read()
        ti.xcom_push(key="sql_content", value=sql_content)

        print(f"SQL file generated at: {sql_path}")

    except FileNotFoundError:
        print("File not found: /tmp/wiki/wikipageviews")
        raise
    except IOError as e:
        print(f"IOError: {e}")
        raise

# Task to fetch pageviews
fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Meta"}},
    provide_context=True,
    dag=dag,
)

# Task to load the data into PostgreSQL
write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    sql="{{ task_instance.xcom_pull(task_ids='fetch_pageviews', key='sql_content') }}",  # Pull the SQL content
    postgres_conn_id="postgres",
    autocommit=True,
    dag=dag,
)

# Task dependencies
get_data >> extract_gz >> fetch_pageviews >> write_to_postgres
