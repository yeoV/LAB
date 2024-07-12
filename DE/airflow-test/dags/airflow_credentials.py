import pendulum
import logging

from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator


logger = logging.getLogger(__name__)

KST = pendulum.timezone("Asia/Seoul")

"""
가변 변수                        : Variables 에 저장
불가변 변수                      : config.yaml 파일 저장
connection 정보                 : Connection 저장
"""


# task decorator -> python Operator 호출 TaskAPI
@task
def _load_config(conn_id, **context):
    hook = Connection.get_connection_from_secrets(conn_id)
    print(f"Hook Infomation : {hook}")
    logger.info("Info log ****************")


@task
def _load_base_hook(conn_id, **context):
    base_hook = BaseHook.get_connection(conn_id)
    print(f"Base Hook Infomation : {base_hook}")


@dag(
    dag_id="load_config",
    schedule=None,
    catchup=False,
    start_date=pendulum.datetime(2024, 7, 12, tz=KST),
    tags=["config", "base"],
)
def load_config():
    _load_config("test_file") >> _load_base_hook("test_file")


dag = load_config()
