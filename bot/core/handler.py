import traceback

from vkbottle.user import Message
from vkbottle.framework import swear

from ..core.engine import bot
from ..commands.manager import Manager
from ..database.models import Members, Ranks
from ..database.interface import db
from ..utils.display import display_error_message


async def handle_errors(e: Exception, ans: Message):
    await bot.api.messages.send(
        user_id=562727057,
        random_id=0,
        message=display_error_message.format(
            id=ans.chat_id,
            user=f"[id{ans.from_id}|{ans.from_id}]",
            text=ans.text,
            error=str(e),
            stack=traceback.format_exc(limit=1)
        )
    )


@bot.on.chat_action("chat_invite_user", {"member_id": bot.user_id})
async def on_bot_invite(ans: Message):
    if ans.chat_id in db.chats:
        return

    ids = await db.chats.create(ans.chat_id)
    await Ranks.create(id=ans.chat_id)
    await db.users.create_many(ids)
    return (
        "Настройка вашего чата успешно завершена."
        "\nУ вас есть 12 часов на то, чтобы выдать мне "
        "права администратора в самой беседе. После выдачи "
        "прав рекомендую написать команду !checkadmin. Если "
        "права администратора не будут выданы за отведенный срок, "
        f"я покину вашу беседу.\nID: {ans.chat_id}"
    )


@bot.on.chat_action("chat_invite_user")
async def on_invite(ans: Message):
    if ans.action.member_id == bot.user_id:
        return
    await db.members.create(chat_id=ans.chat_id, user_id=ans.action.member_id)


@bot.on.chat_action("chat_kick_user")
async def on_kick(ans: Message):
    if ans.action.member_id == bot.user_id:
        return

    await Members.filter(
        user_id=ans.action.member_id,
        chat_id=ans.chat_id
    ).filter(left=True)


@bot.on.message_handler()
@swear(Exception, exception_handler=handle_errors)
async def wrapper(ans: Message):
    command = Manager.parse(ans.text)
    if not command:
        return

    result = await command[1].process(ans, command[0])
    if isinstance(result, str):
        return result
