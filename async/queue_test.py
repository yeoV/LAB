# RAII 를 생각하며 객체의 생성 소멸을 고려하며 만들어 볼것.
import asyncio
from asyncio import Task
from collections import defaultdict, deque
from enum import Enum
import random
import functools

TASK_QUEUE: deque[asyncio.Future[int]] = deque()
STATUS_DICT = defaultdict(int)
RESULT_DICT = defaultdict(int)


class Status(Enum):
    START = 1
    CANCELLED = 2
    SUCCESS = 3


async def task(name: str) -> int:
    delay = random.randint(1, 5)

    print(f"[{name}] Started")

    for sec in range(delay):
        print(f"<{name}>[{sec}s / {delay}s]")
        await asyncio.sleep(1)

    return delay


# 순수 task 만 실행 후, task 반환 (future 상속)
async def task_runner(name) -> Task:
    return asyncio.create_task(task(name))


def set_status(future_name, future: asyncio.Future[int]):
    if future.cancelled():
        print(f"[{future_name}] is cancelled.")
        STATUS_DICT[future_name] = Status.CANCELLED.value
        RESULT_DICT[future_name] = -1

    else:
        print(f"[{future_name}] is successed")
        STATUS_DICT[future_name] = Status.SUCCESS.value
        RESULT_DICT[future_name] = future.result()


"""
task 생성 함수 호출, 큐 삽입 및 관리 모두 여기 메소드에서 관리
- 큐 소유권 가지고 있기 -> 타 함수에 소유권 왔다갔다 별로 (Rust나 C 였으면 지옥)
"""


async def main():
    for idx in range(3):
        name = f"task-{idx}"

        future = await task_runner(name)
        future.set_name(name)
        future.add_done_callback(functools.partial(set_status, name))

        TASK_QUEUE.append(future)

    results = await asyncio.gather(*TASK_QUEUE)
    print(f"All task is finished. {results}")
    print(f"Status dict : {STATUS_DICT}")
    print(f"Result dict : {RESULT_DICT}")


asyncio.run(main())

