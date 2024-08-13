"""
DAG CONFIG 값 Pydantic으로 정합성 check
"""

from __future__ import annotations

import logging
from typing import Dict, Union
from pydantic import BaseModel, ValidationError

from lib import load_config

logger = logging.getLogger(__name__)


class ThirdConfig(BaseModel):
    test_conv: str


class PathConfig(BaseModel):
    hancom_conv_hdfs_path: str
    hdfs_conv_path: str
    test_config: ThirdConfig


class Work(BaseModel, extra="forbid"):
    task_name: str
    sub_task_type: str
    path_config: PathConfig

    @staticmethod
    def safe_load(config_path) -> Dict[str, Union[str, Dict]]:
        try:
            # print(load_config(config_path))
            return Work(**load_config(config_path)).model_dump()
        except ValidationError as e:
            logging.error(f"Mismatch config file and class fields..\n {e}")
