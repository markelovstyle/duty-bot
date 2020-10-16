import bot.database.interface as interface

from inspect import getmembers, ismethod
from asyncio import gather
from typing import (
    List,
    Callable,
    Dict,
    Union
)
from vkbottle.user import Message


class Inspector:
    def __init__(self):
        self.validators: List[Callable] = list()
        self.queue: Dict[int, str] = dict()

    async def check_access(self, ans: Message, code: int):
        user_id, chat_id = ans.from_id, ans.chat_id
        rank = await interface.db.members.get(user_id=user_id, chat_id=chat_id)
        if rank < interface.db.chats[chat_id][code]:
            self.queue[chat_id] = "Недостаточно прав для применения этой команды."

        return True

    async def run(self, ans: Message, code: int) -> Union[str, bool]:
        result = await gather(*[i(ans, code) for i in self.validators])
        if all(result):
            return True

        return self.queue.pop(ans.chat_id)

    def pack(self):
        for k, v in getmembers(self, predicate=ismethod):
            if k not in ('__init__', 'pack', 'run'):
                self.validators.append(v)


