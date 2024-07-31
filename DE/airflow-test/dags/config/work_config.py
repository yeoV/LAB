import logging

from pydantic import BaseModel, ValidationError
from lib import load_config

logger = logging.getLogger(__name__)


class PathConfig(BaseModel):
    hancom_conv_hdfs_path: str
    hdfs_conv_path: str


class Work(BaseModel, extra="forbid"):
    task_name: str
    sub_task_type: str
    path_config: PathConfig

    @staticmethod
    def safe_load(config_path):
        try:
            # print(load_config(config_path))
            return Work(**load_config(config_path))
        except ValidationError as e:
            logging.error(f"Mismatch config file and class fields..\n {e}")
