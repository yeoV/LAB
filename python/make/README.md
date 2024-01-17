## Python MAKE 사용하는 방법

- Although you cannot compile these modules using make,
you can still use make for automation **tasks like running tests**, **installing dependencies**, **cleaning the .pyc files** etc.

- <https://earthly.dev/blog/python-makefile/>

- `.phony`
  - 만약 target 과 동일한 파일 이름이 있는 경우, 항상 최신것으로 간주해서 레시피 수행하지 않는다.!
  - 그럴 경우, target명에 .phony를 명시해줄 경우 해결된다.!
  - 추가로, 병렬 수행도 가능해짐!

- Makefile 작성 법

```
target: pre-req1 pre-req2 pre-req3 ...
    recipes
    ...
```

- target : 빌드에서 생성되어야 하는 파일.
- req : 달성되어야 할 전제 조건
- recipres : 수행되어야 할 명령어 목록

- 수행 절차
  - make가 수행될 때, 전제 조건들을 살펴봄.
  - recipes 가지고 있으면, 모두 수행된 후 타겟 생성 수행.
  - **각 타겟에 대해, 타겟이 존재하지 않거나 전제 조건들이 타겟보다 새로운 경우에만 실행됨.!**
