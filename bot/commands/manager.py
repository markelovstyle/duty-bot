import os

from re import IGNORECASE
from typing import List, Tuple, Optional, Type

from vkbottle.user import Message
from vkbottle.utils import logger
from vbml import Pattern, Patcher

from .abc import Command, CommandException
from .enum import Mode
from ..database.models import Commands, Chat
from ..database.interface import db


class Manager:

    commands: List["Manager"] = list()

    def __init__(
        self,
        uid: int,
        name: str,
        description: str,
        handler: Type[Command],
        accessibility: str,
        patterns: List[str],
        access_code: int = 100,
        lower: bool = True
    ):
        # Sign assets
        self.uid = uid
        self.name = name
        self.description = description

        self.type: Mode = Mode(accessibility)
        self.flag = IGNORECASE if lower else None
        self.patterns = self.serialize(patterns)

        self.patcher: Patcher = Patcher.get_current()
        self.handler: Type[Command] = handler

        self.access_code = access_code

    async def process(self, message: Message, args: dict):
        command = self.handler(message=message, args=args)

        if self.type is Mode.ONLY_USER and not command.sender:
            return os.getenv("ONLY_USER")

        if self.type is Mode.ONLY_CHAT and command.sender:
            return os.getenv("ONLY_CHAT")

        return await command.start()

    def parse_args(self, text: str) -> dict:
        for pattern in self.patterns:
            if self.patcher.check(text, pattern) is not None:
                return pattern.dict()

    def serialize(self, patterns: List[str]) -> List[Pattern]:
        return [
            Pattern(pattern, flags=self.flag)
            for pattern in patterns
        ]

    @classmethod
    def parse(cls, text: str) -> Optional[Tuple[dict, "Manager"]]:
        for command in cls.commands:
            args = command.parse_args(text)
            if args is None:
                continue

            return args, command

    @classmethod
    def get_default(cls) -> dict:
        return {
            command.uid: command.access_code
            for command in cls.commands
        }


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