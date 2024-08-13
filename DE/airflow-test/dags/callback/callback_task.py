# Task 혹은 DAG에 callback 함수를 둬서
import pendulum

from airflow.decorators import dag, task
from airflow.decorators.python import python_task
from airflow.operators.python import PythonOperator

KST = pendulum.timezone("Asia/Seoul")


def task_success_alert(context):
    print(f"Task has successed. run id {context['task_instance_key_str']}")


def task_failure_alert(context):
    print(f"Task has failed. run id {context['task_instance_key_str']}")


@python_task(on_success_callback=task_success_alert)
def _success_task():
    print("Success job is running")


@task(on_failure_callback=task_failure_alert)
def _failure_task():
    print("Fail job is runnßing")
    raise KeyError


@dag(
    dag_id="callback-task",
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 15, tz=KST),
    tags=["callback"],
    # on_success_callback=task_success_alert,
    # on_failure_callback=task_failure_alert,
)
def main():
    _success_task() >> _failure_task()


main()
