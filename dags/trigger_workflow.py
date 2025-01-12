import airflow.utils.dates
from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.dummy import DummyOperator
from pathlib import Path

dag = DAG(
    dag_id = "trigger_workflow",
    start_date = airflow.utils.dates.days_ago(3),
    schedule_interval = "0 16 * * *",
    description = "Workflow for ingesting supermarket promotions data, using FileSensor.",
    default_args = {"depends_on_past": True,}
)

create_metrics = DummyOperator(task_id = "create_metrics", dag = dag)


# Check data abailable:
def _wait_for_supermarket(supermarket_id):
    # Construir la ruta para el supermercado basado en supermarket_id
    supermarket_path = Path(f"/tmp/data/market_data/{supermarket_id}")

    # Verificar si la carpeta existe
    if not supermarket_path.exists():
        print(f"The path {supermarket_path} does not exist.")
        return False

    # Recoger archivos data_*.csv en la ruta (no data-*.csv)
    data_files = list(supermarket_path.glob("data_*.csv"))  # Cambiar el patrón de búsqueda

    # Recoger archivos que terminen en .Zone.Identifier
    identifier_files = list(supermarket_path.glob("data_*.csv:Zone.Identifier"))  # Cambiar el patrón de búsqueda

    # Intentar realizar la verificación de archivos
    try:
        # Mostrar el estado de los archivos encontrados
        print(f"Checking path: {supermarket_path}")
        print(f"Found data files: {data_files}")
        print(f"Found Zone.Identifier files: {identifier_files}")

        # Verificar si ambos archivos están presentes
        if data_files and identifier_files:
            return True  # Ambos archivos de datos y archivos de identificadores existen
        else:
            print("Required files not found.")
            return False  # Faltan archivos de datos o archivos de identificadores

    except Exception as e:
        # Capturar cualquier excepción y mostrar el error
        print(f"An error occurred: {e}")
        return False  # Devolver False en caso de excepción





# Dynamically create tasks for supermarkets 1 through 4
for supermarket_id in range(1, 5):
    wait = PythonSensor(
        task_id=f"wait_for_supermarket_{supermarket_id}",
        python_callable=_wait_for_supermarket,
        op_kwargs={"supermarket_id": f"supermarket_{supermarket_id}"},
        timeout=600,
        dag=dag,
    )
    copy = DummyOperator(task_id=f"copy_raw_supermarket_{supermarket_id}", dag=dag)
    process = DummyOperator(task_id=f"process_supermarket_{supermarket_id}", dag=dag)

    # Define task dependencies
    wait >> copy >> process >> create_metrics


# wait = FileSensor(
#     task_id = "Wait_for_supermarket_data_1",
#     filepath = "tmp/market_data/supermarket_1/data.csv",
#     dag = dag
# )
# 
# wait

