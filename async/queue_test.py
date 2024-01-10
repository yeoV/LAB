import asyncio
import random
from enum import Enum
from collections import defaultdict, deque
import functools

# 현재 수행되고 있는 큐 리스트
TASK_QUEUE: deque[asyncio.Future[None]] = deque()
STATUS_DICT = defaultdict(str)


class Status(Enum):
    START = 1
    CANCELLED = 2
    SUCCESS = 3


# 랜덤으로 몇초간 delay 주는 task
async def task():
    delay = random.randint(1, 5)
    await asyncio.sleep(delay)


async def task_run(idx):
    fut = asyncio.create_task(task())
    fut.set_name(f"task-{idx}")
    TASK_QUEUE.append(fut)
    # task 종료 시, set_status 함수 호출
    fut.add_done_callback(functools.partial(set_status, fut.get_name()))


async def main():
    for idx in range(3):
        print(f"task-{idx} is started")
        await task_run(idx)
        # future 객체 생성 필요 시, get_event_loop() 받아서 생성
        # 그래서 계속 cancel 상태로 반환해버림
        # 해결 방법을 모르겠음 ㅠㅠ
    results = await asyncio.gather(*TASK_QUEUE)
    print(f"All Task is completed. {results}")
    print(f"Status dict : {STATUS_DICT}")


def set_status(
    future_name,
    future: asyncio.Future[None],
):
    if future.cancelled():
        print(f"Task was cancelled. {future_name}")
        STATUS_DICT[future_name] = Status.CANCELLED.value
    else:
        print(f"Task completed successfully.{future_name}")
        STATUS_DICT[future_name] = Status.SUCCESS.value


asyncio.run(main())
