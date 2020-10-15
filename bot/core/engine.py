import os
from asyncio import get_event_loop

from dotenv import load_dotenv
from vkbottle.user import User
from vkbottle.utils import logger

from . import include_routers
from .processor import Processor

from ..commands import include_commands
from ..database.interface import db
from ..utils.validator import patcher
from ..utils.vk import bp

load_dotenv(encoding="utf-8")

loop = get_event_loop()
bot = User(
    tokens=os.getenv("ACCESS_TOKENS").split(","),
    user_id=int(os.getenv("USER_ID")),
    loop=loop,
    vbml_patcher=patcher,
    debug=os.getenv("LOGGER_LEVEL")
)
bot.deconstructed_handle = Processor(bot.user_id, True)
bot.set_blueprints(bp)


def start():
    loop.run_until_complete(db.start())
    loop.create_task(include_commands())
    loop.create_task(bot.run())

    logger.info("Configure handlers...")
    include_routers()

    loop.run_forever()
