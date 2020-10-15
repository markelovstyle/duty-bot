import os

from dotenv import load_dotenv
from tortoise import Tortoise
from vkbottle.utils import logger

from ..utils.mixin import ContextInstanceMixin
from .methods import *

load_dotenv(encoding="utf-8")


class AsyncDB(ContextInstanceMixin):
    def __init__(self):
        self.chats = ChatDict()
        self.members = MembersDict()
        self.users = UsersDict()

    async def start(self):
        try:
            await Tortoise.init(
                db_url=self.get_url(),
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
        for k in self.__dict__:
            await getattr(self, k).load()

    @staticmethod
    def get_url() -> str:
        mapping = {
            "sqlite": "sqlite://{path}",
            "mysql": "mysql://{user}:{password}@{host}:3306/{name}",
            "postgres": "postgres://{user}:{password}@{host}:5432/{name}"
        }
        return mapping[os.getenv("DB_TYPE")].format(
            path=os.getenv("DB_PATH"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            name=os.getenv("NAME")
        )


db = AsyncDB()
AsyncDB.set_current(db)