from __future__ import annotations

import os
from typing import Dict, Union
from sub_task import sub_task
from config.work_config import Work

from airflow.models.connection import Connection
from airflow.decorators import dag, task

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
CONFIG_FILE = f"{AIRFLOW_HOME}/config/work.yaml"


@dag(dag_id="work_dag")
def run_dag():

    # Pydantic config load
    @task
    def load_config():
        config_data: Dict[str, Union[str, dict]] = Work.safe_load(
            CONFIG_FILE
        ).model_dump()
        return config_data

    # Use config value
    @task
    def use_config(config_data, **context):
        task_name = config_data["path_config"]
        print(task_name)

    @task
    def connection_uri():
        conn = Connection.get_connection_from_secrets("elasticsearch_default")
        test = conn.get_uri()
        print(test)

    config = load_config()
    use_config_task = use_config(config)
    # 밖 task 사용 가능 유무 테스트
    sub_task() >> config >> use_config_task >> connection_uri()


run_dag()
