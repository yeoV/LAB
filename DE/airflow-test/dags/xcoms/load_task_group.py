import os
from typing import Dict, Union
from dags.subtask_group.subtask_dummy import sub_task
from config.work_config import Work

from airflow.models.connection import Connection
from airflow.decorators import dag, task

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
CONFIG_FILE = f"{AIRFLOW_HOME}/config/work.yaml"


@dag(dag_id="load_task_group", tags=["xcoms"])
def load_task_group():

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
        conn = Connection.get_connection_from_secrets("hdfs_default")
        print(f"ES Connection info {conn.as_json()}")
        print(f"ES Connection info {conn.get_uri()}")

    config = load_config()
    use_config_task = use_config(config)
    # 밖 task 사용 가능 유무 테스트
    sub_task() >> config >> use_config_task >> connection_uri()


load_task_group()
