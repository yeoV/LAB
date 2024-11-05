import mlflow


# Creating Child Runs
with mlflow.start_run() as parent_run:
    param = [0.01, 0.02, 0.03]

    for p in param:
        with mlflow.start_run(nested=True) as child_run:
            mlflow.log_param("p", p)
