### Multi-Processing

- 별도의 프로세스에서 동작하므로, `mlflow.start_run()` 을 단순히 호출 하면 됨!

### Multi-Threading

- **MLflow는 state 추적을 위해 전역 상태를 사용**함! -> 데이터 손상이 발생 할 수 있음
- Child Runs 방법을 사용해서 해당 문제를 피할 수 있다.

### Child Run

- Single Run 에서 Multiple Run 을 사용할 수 있음!
- Child Run을 사용해서 스레드 간 데이터 간섭 없이 수행 가능함.!
- 사용처 : *hyperparameter tuning, cross-validation folds* ... 등등 최적의 모델을 찾기 위한 실험에 사용
- `nested=True`
-

```python
with mlflow.start_run() as parent_run:
    param = [0.01, 0.02, 0.03]

    # Create a child run for each parameter setting
    for p in param:
        with mlflow.start_run(nested=True) as child_run:
            mlflow.log_param("p", p)
```

##### 컨택스트 중첩

- 동일한 스레드 내에서 실행 컨텍스트를 중첩하여 여러 MLflow 실행을 관리하는 것
- 실행의 계층적 구조를 만들어 부모-자식 관계로 구성
- **부모 실행에서 시작된 자식 실행은 부모 컨텍스트를 상속 -> 자식 실행 로그 데이터는 자식에만 속함**

- TODO `nested=True` 코드 뜯어보기

#### 참고 URL

<https://mlflow.org/docs/latest/tracking/tracking-api.html#sequential-runs>

<https://mlflow.org/docs/latest/tracking/tracking-api.html#child-runs>
