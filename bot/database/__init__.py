import typing

from abc import ABC, abstractmethod


class ABCDict(ABC, dict):
    @abstractmethod
    async def create(self, **kwargs):
        ...

    @abstractmethod
    async def change(self, **kwargs):
        ...

    @abstractmethod
    async def delete(self, **kwargs):
        ...

    @abstractmethod
    async def load(self):
        ...
