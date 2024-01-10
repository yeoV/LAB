# asyncio 맛보기
- python 3.11
- asyncio 라이브러리 사용

### 구현 내용
- async_basic
  - 아래 메소드 활용 방법 
  - create_task(), await, add_done_callback 
  - create_task vs await 생각 할 것!


- semaphore_future
  - future, get_event_loop 를 활용한 세마포어 구현
  - 주의 점 : future를 통해서 wait 할 수 있는 방법 생각
  - relase 시,set_result로 결과 넘겨 줌


- queue_test
  - 3개의 task를 코루틴으로 수헹
  - 각각의 작업이 완료 되었을 경우, 전역 변수 DICT에 task 완료 여부 명시


***
참고  : https://tech.buzzvil.com/blog/asyncio-no-2-future/
