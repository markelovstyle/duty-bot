import os

from re import IGNORECASE
from typing import List, Tuple, Optional, Type

from vkbottle.user import Message
from vkbottle.utils import logger
from vbml import Pattern, Patcher

from .abc import Command, CommandException
from .enum import Accessibility
from database.models import Commands


class Manager:

    commands: List["Manager"] = list()

    def __init__(
        self,
        name: str,
        description: str,
        handler: Type[Command],
        accessibility: str,
        patterns: List[str],
        lower: bool = True
    ):
        # Sign assets
        self.name = name
        self.description = description
        self.type: Accessibility = Accessibility(accessibility)

        self.patcher: Patcher = Patcher.get_current()
        self.flag = IGNORECASE if lower else None
        self.patterns = self.serialize(patterns)

        self.handler: Type[Command] = handler

    async def start(self, message: Message, args: dict):
        command = self.handler(message=message, args=args)

        if command.type.FROM_CHAT and self.type.ONLY_USER:
            return command.answer(os.getenv("ONLY_USER"))

        if command.type.FROM_USER and self.type.ONLY_CHAT:
            return command.answer(os.getenv("ONLY_CHAT"))

        await command.start()

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
        lowered = text.lower()
        for command in cls.commands:
            if not lowered.startswith(command.name.lower()):
                continue

            args = command.parse_args(text)
            if not args:
                continue

            return args, command


def register_command(**kwargs):
    if await Commands.exists(name=kwargs.get("name")):
        raise CommandException("Command with this name already exists!")

    Manager.commands.append(Manager(**kwargs))
    kwargs.pop("handler")
    await Commands.create(**kwargs)

    logger.info("Command {} has been registered!", kwargs.get("name"))
