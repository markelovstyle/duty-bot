from vkbottle.user import Blueprint, Message
from ..commands.manager import Manager

dp = Blueprint(name="Handlers")


@dp.on.message_handler()
async def wrapper(ans: Message):
    command = Manager.parse(ans.text)
    if not command:
        return

    result = await command[1].process(ans, command[0])
    if isinstance(result, str):
        return result