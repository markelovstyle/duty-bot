from vkbottle.user import Blueprint, Message
from vkbottle.rule import ChatActionRule

from .middlewares import Register, db
from ..commands.manager import Manager
from ..database.models import Members

dp = Blueprint(name="Handlers")


@dp.on.chat_message(ChatActionRule("chat_invite_user"))
async def on_invite(ans: Message):
    if ans.action.member_id != dp.api.user_id:
        return await Members.get_or_create(
            user_id=ans.action.member_id,
            chat_id=ans.chat_id
        )

    if ans.chat_id in db.accesses:
        return

    await Register().pre(ans)
    await ans("Новый чат!")


@dp.on.chat_message(ChatActionRule("chat_kick_user"))
async def on_kick(ans: Message):
    if ans.action.member_id == dp.api.user_id:
        return

    await Members.filter(
        user_id=ans.action.member_id,
        chat_id=ans.chat_id
    ).filter(left=True)


@dp.on.message_handler()
async def wrapper(ans: Message):
    command = Manager.parse(ans.text)
    if not command:
        return

    result = await command[1].process(ans, command[0])
    if isinstance(result, str):
        return result