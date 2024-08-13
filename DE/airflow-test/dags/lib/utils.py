import yaml
import logging
import datetime
import json
from typing import Dict
from jinja2 import Template, Environment, FileSystemLoader

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
def load_config(config_path: str) -> Dict[str, str]:
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"[Error] Fail load common config.File path : {config_path}")
        raise e


# Jinja template Rendering
def rendering_config(config_path, date):
    with open(config_path) as f:
        template_content: str = f.read()
    # Environment class 로 만듬
    template = Template(template_content)
    # 변수로 넣을 값 load
    pre_rendered_config = yaml.safe_load(template_content)
    # template 에 변수값 rendereing
    rendered_config: str = template.render(pre_rendered_config, date=date)
    return yaml.safe_load(rendered_config)


def get_current_date():
    return datetime.datetime.now().strftime("%Y%m%d")


def load_es_config():
    conn = Connection.get_connection_from_secrets(CONNECTIONS["ES"])
    # http -> https
    secure_uri = "https" + conn.get_uri()[4:]
    return Elasticsearch(secure_uri, api_key=conn.get_password(), verify_certs=False)


def load_hdfs_config():
    conn = Connection.get_connection_from_secrets(CONNECTIONS["HDFS"])
    return InsecureClient(conn.get_uri(), conn.login)


if __name__ == "__main__":
    temp = rendering_config("config/work.yaml", get_current_date())
    print(temp)
    # test_rendering("config/work.yaml", get_current_date())
