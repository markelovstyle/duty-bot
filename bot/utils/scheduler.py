import asyncio

from typing import Coroutine
from .enum import TaskType


class Scheduler:
    @staticmethod
    async def run_disposable_task(func: Coroutine, time: int):
        await asyncio.sleep(time)
        return await func

    @staticmethod
    async def run_periodic_task(func: Coroutine, time: int):
        while True:
            await asyncio.sleep(time)
            await func

    @classmethod
    def create_task(cls, func: Coroutine, time: int, task_type: TaskType):
        loop = asyncio.get_running_loop()
        if task_type is TaskType.DISPOSABLE:
            loop.create_task(cls.run_disposable_task(func, time))

        if task_type is TaskType.PERIODIC:
            loop.create_task(cls.run_periodic_task(func, time))
