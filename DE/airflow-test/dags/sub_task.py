from airflow.decorators import task, task_group
from airflow.operators.empty import EmptyOperator

test = "{hello} HELLO WORLD {world}"


@task_group(group_id="Task-Group")
def sub_task():
    task1 = EmptyOperator(task_id="task1")
    task2 = EmptyOperator(task_id="task2")
    task3 = EmptyOperator(task_id="task3")
    task1 >> [task2, task3]
