from vkbottle.utils import logger

from .abc import CommandException
from .blueprints.accesses import Accesses
from .blueprints.help import Help
from .blueprints.change_access import ChangeAccess
from .manager import Manager

from ..database.interface import db
from ..database.models import Commands, Chat


async def register_command(**kwargs):
    if any([i for i in Manager.commands if i.name == kwargs["name"]]):
        raise CommandException("Command with this name already exists!")

    save = await Commands.get_or_create(
        name=kwargs["name"],
        description=kwargs["description"],
        type=kwargs.get("accessibility", "all"),
        access_code=kwargs.get("access_code", 5)
    )
    if save[1]:
        for k, v in db.chats.items():
            db.chats[k].update({save[0].id: save[0].access_code})
            await Chat.filter(id=k).update(accesses=db.chats[k])

    Manager.commands.append(Manager(**kwargs, uid=save[0].id))
    logger.info(
        "Command «{name}» with UID {uid} has been registered!",
        name=kwargs.get("name"), uid=save[0].id
    )


async def include_commands():
    await register_command(
        access_code=0,
        name="Помощь",
        description="Навигация по всему функционалу бота",
        handler=Help,
        accessibility="all",
        patterns=["помощь", "команды"]
    )
    await register_command(
        access_code=0,
        name="Доступы",
        description="Выводит список всех доступов команд",
        handler=Accesses,
        accessibility="only_chat",
        patterns=["доступы"]
    )
    await register_command(
        access_code=4,
        name="Доступ",
        description="Изменяет доступ команды",
        handler=ChangeAccess,
        accessibility="only_chat",
        patterns=["<cmd> доступ <code:int>", "<cmd:int> доступ <code:int>"]
    )