import yaml
import logging
import datetime
from typing import Dict

from hdfs import InsecureClient
from elasticsearch import Elasticsearch

from airflow.decorators import task
from airflow.models.connection import Connection

# 전역 변수 -> Variables 로 빼기?
COMMON_CONFIG_PATH = ""

# default level : info
# Logger도 전역에서 제거하는 것이 좋은지??
logger = logging.getLogger(__name__)

CONNECTIONS = {"ES": "elasticsearch_default", "HDFS": "hdfs_default"}


# Load config task
def load_common_config(config_path: str) -> Dict[str, str]:
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"[Error] Fail load common config.File path : {config_path}")
        raise e


def get_current_date():
    return datetime.now().strftime("%Y%m%d")


def load_es_config():
    conn = Connection.get_connection_from_secrets(CONNECTIONS["ES"])
    return Elasticsearch(
        conn.get_uri(), api_key=conn.get_password(), verify_certs=False
    )


def load_hdfs_confug():
    conn = Connection.get_connection_from_secrets(CONNECTIONS["HDFS"])
    return InsecureClient(conn.get_uri(), conn.login)
