import os
from typing import Dict, List

from dotenv import load_dotenv
from tortoise import Tortoise
from vkbottle.utils import logger

from .models import Chat, Users, Members
from ..utils.mixin import ContextInstanceMixin
from ..utils.vk import get_chat_data
from ..commands.manager import Manager

load_dotenv(encoding="utf-8")


class AsyncDB(ContextInstanceMixin):
    def __init__(self):
        self.db_connections: Dict[str, str] = {
            "sqlite": "sqlite://{path}",
            "mysql": "mysql://{user}:{password}@{host}:3306/{name}",
            "postgres": "postgres://{user}:{password}@{host}:5432/{name}"
        }
        self.accesses = dict()
        self.users = dict()

    async def register_chat(self, chat_id: int):
        data = await get_chat_data(chat_id)
        save = await Chat.create(
            id=chat_id, title=data[0],
            owner_id=data[1], accesses=Manager.get_default()
        )
        await self.insert_users(chat_id, data[2])
        db.accesses.update(save.load_model())
        logger.info(
            "Chat «{title}» with ID {id} has registered!",
            title=data[0], id=chat_id
        )

    @staticmethod
    async def insert_users(chat_id: int, users: List[int]):
        await Members.bulk_create(objects=[
            Members(user_id=user, chat_id=chat_id)
            for user in users
        ])

    async def start(self):
        try:
            await Tortoise.init(
                db_url=self.db_connections[os.getenv("DB_TYPE")].format(
                    path=os.getenv("DB_PATH"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASSWORD"),
                    host=os.getenv("HOST"),
                    name=os.getenv("NAME")
                ),
                modules={'models': ['bot.database.models']}
            )
            await Tortoise.generate_schemas(safe=True)
            logger.info(
                "Successfully connected to the database: {}://{}",
                os.getenv("DB_TYPE"), os.getenv("HOST")
            )
        except Exception as e:
            logger.exception(e)

        return await self.load()

    async def load(self):
        async for i in Chat.all():
            self.accesses.update(i.load_model())

        async for user in Users.all():
            self.users.update(user.load_model())


db = AsyncDB()
AsyncDB.set_current(db)