# https://tech.buzzvil.com/blog/asyncio-no-2-future/
import asyncio
from abc import ABCMeta
from datetime import datetime
from collections import deque


class Semaphore(metaclass=ABCMeta):
    _value: int

    def __init__(self, initial_value: int = 1) -> None:
        self._value = initial_value

    # busy waiting 방식
    async def acquire(self) -> None:
        raise NotImplementedError

    def release(self) -> None:
        raise NotImplementedError


"""
Busy-waiting Semaphore
"""


class BusywaitingSemaphore(Semaphore):
    # busy waiting 방식
    # 0.1 초씩 sleep 하면서 기다리기 때문에 release타이밍과 안맞을 수도 있음
    async def acquire(self) -> None:
        while self._value <= 0:
            await asyncio.sleep(0.1)
        self._value -= 1

    def release(self) -> None:
        self._value += 1


"""
Future 방식 Semaphore
"""


class FutureSemaphore(Semaphore):
    _queue: deque[asyncio.Future[None]]

    def __init__(self, initial_value: int = 1) -> None:
        super().__init__(initial_value)
        self._queue = deque()

    async def acquire(self):
        if self._value <= 0:
            loop = (
                asyncio.get_event_loop()
            )  # event loop 은 언제나 싱글스레드 기반이기에, single thread 기반 한정 안전함
            fut = loop.create_future()  # 기다릴 퓨처 생성
            self._queue.append(fut)
            await fut

        self._value -= 1

    def release(self) -> None:
        self._value += 1
        if len(self._queue) > 0:
            fut: asyncio.Future = self._queue.popleft()
            fut.set_result(None)


async def run_job(sem: Semaphore, job_id: int) -> None:
    # 세마포어 획득
    await sem.acquire()
    print(f"{datetime.now()} - start job {job_id}")
    await asyncio.sleep(1)
    print(f"{datetime.now()} - job {job_id} finished")
    sem.release()


async def main() -> None:
    # 2개 세마포어 생성
    sem = FutureSemaphore(2)

    await asyncio.gather(
        run_job(sem, 1),
        run_job(sem, 2),
        run_job(sem, 3),
        run_job(sem, 4),
        run_job(sem, 5),
    )


asyncio.run(main())
