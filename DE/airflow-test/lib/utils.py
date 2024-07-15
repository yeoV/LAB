import yaml
import logging

from airflow.decorators import task

# 전역 변수 -> Variables 로 빼기?
COMMON_CONFIG_PATH = ""

# default level : info
logger = logging.getLogger(__name__)


# Load config task
def load_common_config(config_path: str):
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"[Error] Fail load common config.File path : {config_path}")
        raise e
