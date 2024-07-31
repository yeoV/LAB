import pendulum
import logging
import datetime

from lib import *
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from airflow.decorators import dag, task


logger = logging.getLogger(__name__)

KST = pendulum.timezone("Asia/Seoul")

"""
가변 변수                        : Variables 에 저장
불가변 변수                      : config.yaml 파일 저장
connection 정보                 : Connection 저장
"""


# task decorator -> python Operator 호출 TaskAPI
@task
def load_es_config():
    es_client = load_es_config()
    logger.info(f"ES Connection : {es_client}")
    print({{op_kwargs}})


@task
def load_hdfs_config():
    hdfs_client = load_hdfs_config()
    logger.info(f"HDFS Client : {hdfs_client}")


@dag(
    dag_id="load_config",
    schedule=None,
    catchup=False,
    start_date=pendulum.datetime(2024, 7, 12, tz=KST),
    tags=["config", "base"],
)
def load_config():

    [load_es_config(), load_hdfs_config()]


dag = load_config()
