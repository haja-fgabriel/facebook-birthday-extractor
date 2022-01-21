from datetime import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 1, 20, 0, 0),
    "retries": 3,
}

dag = DAG(dag_id="scraper_workflow", default_args=default_args, catchup=False, schedule_interval="0 0 * * *")

run_scraper = BashOperator(
    task_id="run_scraper",
    bash_command="/home/airflow/.local/bin/scrapy crawl facebook",
    env={
        "FACEBOOK_EMAIL": os.getenv("FACEBOOK_EMAIL"),
        "FACEBOOK_PASSWORD": os.getenv("FACEBOOK_PASSWORD"),
    },
    dag=dag,
    cwd="/facebook-scraper/src",
)
