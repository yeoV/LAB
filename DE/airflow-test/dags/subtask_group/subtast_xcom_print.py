"""
CASE 1. Operator 를 활용해서 외부 taskapi 에서 데이터 받음
CASE 2. task 데코레이터를 활용해서 xcom 데이터 활용
"""

from airflow.decorators import task, task_group
from airflow.operators.bash import BashOperator


@task_group(group_id="subtast-xcom-print")
def print_xcom_group(config, **context):

    # 아래와 같이 작성하는 경우, XCOM 아래와 같은 식으로 데이터 표현됨
    # {{ task_instance.xcom_pull(task_ids='load_dag_config', dag_id='tg_data_transfer', key='return_value') }
    @task
    def print_task(config):
        print(f"Task Group config : {config}")

    print_task(config=config)
