import glob
import importlib.util
import os
import sys

import pytest
from airflow.models.dag import dag
from airflow.models import DAG

# from airflow.decorators import dag


# ../../dags 하위에 있는 모든 파일들 수집
DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/*.py")

DAG_FILES = glob.glob(DAG_PATH, recursive=True)
# DAG_FILES = glob.glob(DAG_PATH)


@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    print(f"SYS PATH : {sys.path}")
    module_name, _ = os.path.splitext(dag_file)
    # module_path = os.path.join(DAG_PATH, dag_file)
    mod_spec = importlib.util.spec_from_file_location(module_name, dag_file)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    # DAG Object 에 대한 검증
    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]

    for var in vars(module).values():
        if callable(var):
            print(f"VAR : {var}")
            print(var.__get__)

    assert dag_objects
    # dag_funcions = [
    #     var
    #     for var in vars(module).values()
    #     if callable(var) and hasattr(var, "_is_dag")
    # ]

    # assert dag_objects or dag_funcions

    # for dag in dag_objects:
    #     dag.test_cycle()


#  <function dag at 0x107040820>
# ['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
