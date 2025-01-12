import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id = "wikimedia_project",
    # comenzará a ejecutarse 3 días antes de la fecha actual.
    start_date = airflow.utils.dates.days_ago(3),
    # El DAG se ejecutará una vez por hora.
    schedule_interval = "@hourly",
)

get_date = BashOperator(
    task_id = 'get_data',
    bash_command = (
        "curl -o /tmp/wiki/wikipageviews.gz "
        "https://dumps.wikimedia.org/other/pageviews/"
        "{{ execution_date.year }}/"
        "{{ execution_date.year }}-{{ '{:02}'.format(execution_date.month) }}/"
        "pageviews-{{ execution_date.year }}"
        "{{ '{:02}'.format(execution_date.month) }}"
        "{{ '{:02}'.format(execution_date.day) }}-"
        "{{ '{:02}'.format(execution_date.hour-4) }}0000.gz"
    ),
    dag=dag,
)

get_date
