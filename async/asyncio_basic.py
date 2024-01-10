# https://tech.buzzvil.com/blog/asyncio-no-2-future/
import asyncio
import random
from datetime import datetime
import time
import functools


async def run_job():
    delay = random.randint(5, 15)
    await asyncio.sleep(delay)


def print_wall_time(before: float, future: asyncio.Future[None]) -> None:
    after = time.time()
    if future.exception():
        print(f"Error occurred: {future.exception()}, duration: {after-before} sec")
    else:
        print(f"Result: {future.result()}, duration: {after-before} sec")

    print(f" Job duration : {after - before} sec")


async def main():
    while True:
        before = time.time()
        future = asyncio.create_task(run_job())
        # future는 콜백함수 파라미터르 객체 자신을 넘겨줌
        # 단 call_back 함수의 호출 순서를 보장할 순 없음 -> future 실행이 끝난 이후, eventloop ioteration에 콜백 함수 실행 등록
        future.add_done_callback(functools.partial(print_wall_time, before))

        # 코루틴 함수 콜백으로 등록하고 싶은 경우 -> 단 create_task 이므로 코루틴이 종료되는 것을 기다릴 수 없음
        # future.add_done_callback(lambda fut: asyncio.create_task(async 함수 (fut)))
        await asyncio.sleep(1)


asyncio.run(main())
