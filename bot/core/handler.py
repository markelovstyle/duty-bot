from vkbottle.user import Message

from ..core.engine import bot
from ..commands.manager import Manager
from ..database.models import Members
from ..database.interface import db


@bot.on.chat_action("chat_invite_user", {"member_id": bot.user_id})
async def on_invite(ans: Message):
    if ans.chat_id in db.accesses:
        return

    await db.register_chat(ans.chat_id)
    await ans(
        "Настройка вашего чата успешно завершена."
        "\nУ вас есть 12 часов на то, чтобы выдать мне "
        "права администратора в самой беседе. После выдачи "
        "прав рекомендую написать команду !checkadmin. Если "
        "права администратора не будут выданы за отведенный срок, "
        f"я покину вашу беседу.\nID: {ans.chat_id}"
    )


@bot.on.chat_action("chat_kick_user")
async def on_kick(ans: Message):
    if ans.action.member_id == bot.user_id:
        return

    await Members.filter(
        user_id=ans.action.member_id,
        chat_id=ans.chat_id
    ).filter(left=True)


@bot.on.message_handler()
async def wrapper(ans: Message):
    if ans.chat_id not in db.accesses:
        return

    command = Manager.parse(ans.text)
    if not command:
        return

    result = await command[1].process(ans, command[0])
    if isinstance(result, str):
        return result