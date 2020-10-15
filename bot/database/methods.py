from vkbottle.utils import logger
from typing import List, NoReturn

from . import ABCDict
from .models import Chat, Members

from ..commands.manager import Manager
from ..utils.vk import get_chat_data

__all__ = (
    "ABCDict",
    "ChatDict",
    "MembersDict"
)


class ChatDict(ABCDict):
    async def create(self, chat_id: int) -> Chat:
        data = await get_chat_data(chat_id)
        save = await Chat.create(
            id=chat_id, title=data[0],
            owner_id=data[1], accesses=Manager.get_default()
        )
        await MembersDict.insert_users(chat_id, data[2])
        self.update(save.load_model())
        return save

    async def delete(self, **kwargs):
        pass

    async def change(self, **kwargs):
        pass

    async def load(self) -> NoReturn:
        async for i in Chat.all():
            self.update(i.load_model())


class MembersDict(ABCDict):
    async def create(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        raise NotImplementedError

    async def change(self, **kwargs):
        raise NotImplementedError

    async def load(self):
        pass

    @staticmethod
    async def insert_users(chat_id: int, users: List[int]):
        await Members.bulk_create(objects=[
            Members(user_id=user, chat_id=chat_id)
            for user in users
        ])