import os
from typing import Dict

from dotenv import load_dotenv
from tortoise import Tortoise
from vkbottle.utils import logger

from .models import Chat, Users
from ..utils.mixin import ContextInstanceMixin

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