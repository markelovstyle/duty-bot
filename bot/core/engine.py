import os
from asyncio import get_event_loop

from dotenv import load_dotenv
from vkbottle.user import User

from .handler import dp
from .middlewares import mw
from ..commands import include_commands
from ..database.interface import db
from ..utils.validator import patcher

load_dotenv(encoding="utf-8")

loop = get_event_loop()
bot = User(
    tokens=os.getenv("ACCESS_TOKENS").split(","),
    loop=loop,
    vbml_patcher=patcher,
    debug=os.getenv("LOGGER_LEVEL")
)
bot.set_blueprints(dp, mw)


def start():
    loop.run_until_complete(db.start())
    loop.create_task(include_commands())
    loop.create_task(bot.run())
    loop.run_forever()
