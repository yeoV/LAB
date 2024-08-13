import json
from typing import Dict, Tuple, Union

from config.work_config import Work
from lib.utils import load_config, get_current_date

from airflow.decorators import dag, task


@dag(
    dag_id="config_task_dag",
    schedule=None,
    catchup=False,
    tags=["xcoms"],
)
def _config_task_dag():
    DAG_CONFIG_PATH = "config/work.yaml"

    @task(multiple_outputs=True)
    def load_dag_config():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """

        dag_config: Dict = Work.safe_load(DAG_CONFIG_PATH)
        return dag_config

    @task
    def load_history_file(dag_config):
        history_file = f"{dag_config['task_name']}_history.json"
        history_path = "/opt/airflow/logs/shb"
        print(history_file)
        return history_file, history_path

    @task
    def print_task_name(task_name: str) -> None:
        print(f"{task_name}")

    @task
    def print_path_config(path_config):
        hancom_conv_hdfs_path = path_config["hancom_conv_hdfs_path"]
        hdfs_conv_path = path_config["hdfs_conv_path"]

        print(f"hancom_conv_hdfs_path: {hancom_conv_hdfs_path}")
        print(f"hdfs_conv_path : {hdfs_conv_path}")

    @task
    def print_tuple_config(history):
        print(history[0])

    dag_config = load_dag_config()
    # multiple 하게 값을 받을 순 없음. XCOM 으로 리턴받아야함
    file = load_history_file(dag_config)
    print_task_name(dag_config["task_name"])
    print_path_config(dag_config["path_config"])
    print_tuple_config(file)


_config_task_dag()
