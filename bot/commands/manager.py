import os

from re import IGNORECASE
from typing import List, Tuple, Optional, Type

from vkbottle.user import Message
from vkbottle.utils import logger
from vbml import Pattern, Patcher

from .abc import Command, CommandException
from .enum import Mode
from ..database.models import Commands


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
        lower: bool = True
    ):
        # Sign assets
        self.uid = uid
        self.name = name
        self.description = description
        self.type: Mode = Mode(accessibility)

        self.patcher: Patcher = Patcher.get_current()
        self.flag = IGNORECASE if lower else None
        self.patterns = self.serialize(patterns)

        self.handler: Type[Command] = handler

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


async def register_command(**kwargs):
    for command in Manager.commands:
        if command.name == kwargs.get("name"):
            raise CommandException("Command with this name already exists!")

    instance = await Commands.get_or_create(
        name=kwargs["name"],
        description=kwargs["description"],
        type=kwargs.get("accessibility", "all")
    )
    Manager.commands.append(Manager(**kwargs, uid=instance[0].id))
    logger.info(
        "Command «{name}» with UID {uid} has been registered!",
        name=kwargs.get("name"), uid=instance[0].id
    )