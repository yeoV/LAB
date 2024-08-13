"""
1. 외부 taskgroup 에 데이터 전달하기
2. XCOM 데이터 의존성 해결하기
    - TaskGroup 사용
    - DummyOperator
    - Branching
"""

import json
from typing import Dict, Tuple, Union

from task_group.print_xcom_task import print_xcom_group
from config.work_config import Work
from lib.utils import load_config, get_current_date

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator


@dag(
    dag_id="using_branching",
    schedule=None,
    catchup=False,
    tags=["taskgroup_dags"],
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
    def print_local_config(dag_config):
        print(dag_config)

    @task
    def print_local_config2(dag_config):
        print(dag_config)

    @task
    def print_local_config3(dag_config):
        print(dag_config)

    def branch_func():
        return "print_local_config" if dag_config else "another_task"

    # Branching Operator
    branching = BranchPythonOperator(
        task_id="branching",
        python_callable=branch_func,
    )

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    dag_config = load_dag_config()
    t1 = print_xcom_group(dag_config)
    t2 = print_local_config(dag_config)
    t3 = print_local_config2(dag_config)
    t4 = print_local_config3(dag_config)

    start >> dag_config >> branching

    branching >> t1, t2 >> end
    branching >> t3, t4 >> end


_config_task_dag()
