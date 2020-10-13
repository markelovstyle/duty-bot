from .abc import CommandException
from .blueprints.accesses import Accesses
from .blueprints.help import Help
from .manager import Manager

from ..database.interface import db
from ..database.models import Commands, Chat

from vkbottle.utils import logger


async def register_command(**kwargs):
    for command in Manager.commands:
        if command.name == kwargs.get("name"):
            raise CommandException("Command with this name already exists!")

    save = await Commands.get_or_create(
        name=kwargs["name"],
        description=kwargs["description"],
        type=kwargs.get("accessibility", "all"),
        access_code=kwargs.get("access_code", 100)
    )
    if save[1]:
        for k, v in db.accesses.items():
            db.accesses[k].update({save[0].id: save[0].access_code})
            await Chat.filter(id=k).update(accesses=db.accesses[k])

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