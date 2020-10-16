from typing import List, NoReturn, Optional

from . import ABCDict
from .models import *

from ..commands.manager import Manager
from ..utils.vk import get_chat_data, get_users

__all__ = (
    "ABCDict",
    "ChatDict",
    "MembersDict",
    "UsersDict",
    "RanksDict"
)


class ChatDict(ABCDict):
    async def create(self, chat_id: int) -> List[int]:
        data = await get_chat_data(chat_id)
        save = await Chat.create(
            id=chat_id, title=data[0],
            owner_id=data[1], accesses=Manager.get_default()
        )
        await MembersDict.insert_users(chat_id, data[2], data[1])
        self.update(save.load_model())
        return data[2]

    async def delete(self, **kwargs):
        pass

    async def change(self, uid: int, code: int, value: int):
        self[uid][code] = value
        await Chat.filter(id=uid).update(
            accesses=self[uid]
        )

    async def load(self) -> NoReturn:
        async for i in Chat.all():
            self.update(i.load_model())


class MembersDict(ABCDict):
    async def create(self, **kwargs) -> Optional[Members]:
        data = await Members.get_or_create(**kwargs)
        if data[1]:
            return data[0]

        await self.change(False, **kwargs)

    async def get(self, **kwargs) -> int:
        member = await Members.filter(**kwargs).get()
        return member.rank

    async def delete(self, **kwargs):
        raise NotImplementedError

    async def change(self, value: bool, **kwargs) -> NoReturn:
        await Members.filter(**kwargs).update(left=value)

    async def load(self):
        pass

    @staticmethod
    async def insert_users(chat_id: int, users: List[int], owner_id: int):
        await Members.bulk_create([
            Members(user_id=i, chat_id=chat_id, rank=[0, 5][i == owner_id])
            for i in users
        ])


class UsersDict(ABCDict):
    async def create(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass

    async def change(self, **kwargs):
        pass

    async def create_many(self, ids: List[int]):
        users = await get_users(ids)
        filtered = [
            Users(id=user.id, name=f"{user.first_name} {user.last_name}")
            for user in users if user.id not in self
        ]
        await Users.bulk_create(filtered)
        for f in filtered:
            self.update(f.load_model())

    async def load(self):
        async for i in Users.all():
            self.update(i.load_model())


class RanksDict(ABCDict):
    async def create(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass

    async def change(self, chat_id: int, num: int, tag: str):
        self[chat_id][num] = tag
        await Ranks.filter(id=chat_id).update(
            tags=self[chat_id]
        )

    async def load(self):
        async for i in Ranks.all():
            self.update(i.load_model())