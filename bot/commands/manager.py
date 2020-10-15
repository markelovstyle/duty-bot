import os
from re import IGNORECASE
from typing import List, Tuple, Optional, Type

from vbml import Pattern, Patcher
from vkbottle.user import Message

from .abc import Command
from bot.utils.enum import Mode


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
        access_code: int = 5,
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