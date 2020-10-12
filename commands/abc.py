from abc import ABC, abstractmethod
from vkbottle.user import Message
from .enum import Sender


class CommandException(Exception):
    pass


class Command(ABC):
    def __init__(self, *, message: Message, args: dict):
        self.message: Message = message
        self.args = args
        self.type: Sender = self.get_type()

    def get_type(self) -> Sender:
        if self.message.peer_id == self.message.from_id:
            return Sender.FROM_USER

        return Sender.FROM_CHAT

    async def answer(self, text: str, **kwargs) -> int:
        return await self.message(text, **kwargs)

    @abstractmethod
    async def start(self):
        ...
