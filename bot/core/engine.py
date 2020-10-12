import os
from asyncio import get_event_loop

from dotenv import load_dotenv
from vkbottle.user import User

from ..database.interface import db
from ..commands import include_commands
from .handler import dp

load_dotenv(encoding="utf-8")

loop = get_event_loop()
bot = User(
    tokens=os.getenv("ACCESS_TOKENS").split(","),
    loop=loop,
    debug=os.getenv("LOGGER_LEVEL")
)
bot.set_blueprints(dp)


def start():
    loop.run_until_complete(db.start())
    loop.create_task(include_commands())
    loop.create_task(bot.run())
    loop.run_forever()
