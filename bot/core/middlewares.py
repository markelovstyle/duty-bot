from typing import List

from vkbottle.user import Blueprint, Message
from vkbottle.ext import Middleware
from vkbottle.utils import logger

from ..database.models import Chat, Members
from ..database.interface import AsyncDB
from ..commands.manager import Manager

mw = Blueprint(name="Middleware")
db = AsyncDB.get_current()


@mw.middleware.middleware_handler()
class Register(Middleware):
    async def pre(self, ans: Message, *args):
        if ans.chat_id in db.accesses:
            return

        data = await self.get_chat_data(ans.chat_id)
        save = await Chat.create(
            id=ans.chat_id, title=data[0],
            owner_id=data[1], accesses=Manager.get_default()
        )
        await self.insert_users(ans.chat_id, data[2])
        db.accesses.update(save.load_model())
        logger.info(
            "Chat «{title}» with ID {id} has registered!",
            title=data[0], id=ans.chat_id
        )

    @staticmethod
    async def get_chat_data(chat_id: int) -> tuple:
        response = await mw.api.request("messages.getChat", {
            "chat_id": chat_id
        })
        return (
            response["title"],
            response["admin_id"],
            response["users"]
        )

    @staticmethod
    async def insert_users(chat_id: int, users: List[int]):
        await Members.bulk_create(objects=[
            Members(user_id=user, chat_id=chat_id)
            for user in users
        ])
