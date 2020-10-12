from abc import ABC, abstractmethod
from vkbottle.user import Message


class CommandException(Exception):
    pass


class Command(ABC):
    def __init__(self, *, message: Message, args: dict):
        self.message: Message = message
        self.args = args
        self.sender: bool = self.get_sender()

    def get_sender(self) -> bool:
        if self.message.peer_id == self.message.from_id:
            return True

        return False

    async def answer(self, text: str, **kwargs) -> int:
        return await self.message(text, **kwargs)

    @abstractmethod
    async def start(self):
        ...
