from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 1, 21, 19, 0),
}


def execute_first(text):
    print(text)
    return text


with DAG(
    dag_id="helloworld_dag",
    description="Hello World! This is a description",
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    default_args=args,
    tags=["hello", "world", "helloworld"],
    catchup=False,
) as dag:
    execute_first_function = PythonOperator(
        task_id="execute_first_function",
        python_callable=execute_first,
        op_args=["Hello World!"],
    )

if __name__ == "__main__":
    dag.cli()
