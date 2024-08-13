import os
import time
import random

from multiprocessing import Process, Pool, parent_process, current_process

from airflow.decorators import task, dag


def random_sleep():
    sec = random.randint(0, 5)
    time.sleep(sec)
    print(f"Sleep Done : {sec} Sec.")


def initializer():
    current_process().daemon = False


@task(pool="test_pool")
def random_task():
    for _ in range(20):
        random_sleep()


@task
def check_pid():
    # Daemon 에서 자식은 생성할 수 없나?
    print("Start Check pid task ")
    print(
        f" Parent Process : {os.getppid()} is daemon ? : {parent_process().daemon if parent_process() is not None else None} "
    )
    print(f" Current Process : {os.getpid()} is daemon ? : {current_process().daemon} ")
    current_process().daemon = False
    print(f" Current Process : {os.getpid()} is daemon ? : {current_process().daemon} ")


@dag(
    dag_id="multiprocessing_task",
    schedule_interval=None,
    catchup=False,  # 시작 날짜부터 하나씩 수행될 것인지
)
def main():

    check_pid() >> random_task()


main()
