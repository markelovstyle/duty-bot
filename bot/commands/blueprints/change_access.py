from typing import Optional, Union

from ..abc import Command
from ..manager import Manager
from bot.database.interface import AsyncDB

db = AsyncDB.get_current()


class ChangeAccess(Command):
    async def start(self):
        command = self.get_command(self.args["cmd"])
        if not command:
            return

        if self.args["code"] > 5:
            return ("Вы указали неверный номер доступа. "
                    "Диапазон допустимых значений от 0 до 5.")

        await db.chats.change(
            self.message.chat_id, command.uid, self.args["code"]
        )
        return f"Команде <{command.name}> присвоен доступ {self.args['code']}."

    @staticmethod
    def get_command(cmd: Union[int, str]) -> Optional[Manager]:
        for command in Manager.commands:
            if command.name.lower() == cmd:
                return command

            if str(command.uid) == cmd:
                return command
