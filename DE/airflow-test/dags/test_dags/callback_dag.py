import datetime
import pendulum

from airflow import DAG
from airflow.operators.empty import EmptyOperator


def task_failure_alert(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")


def dag_success_alert(context):
    print(f"DAG has succeeded, run_id: {context['run_id']}")


# callback List 로 여러 callback 함수 정의 가능
# 예) on_failure_callback = [func1, func2 . .]
with DAG(
    dag_id="callback_dag",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 10, tz="UTC"),
    dagrun_timeout=datetime.timedelta(minutes=60),
    catchup=False,
    on_success_callback=None,
    on_failure_callback=task_failure_alert,
    tags=["example"],
):
    print(pendulum.timezones)
    task1 = EmptyOperator(task_id="task1")
    task2 = EmptyOperator(task_id="task2")
    task3 = EmptyOperator(task_id="task3", on_success_callback=[dag_success_alert])
    task4 = EmptyOperator(task_id="test4")

    task1 >> [task2, task4] >> task3
