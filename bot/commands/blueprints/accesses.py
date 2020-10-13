from bot.database.interface import AsyncDB
from ..abc import Command
from ..manager import Manager

db = AsyncDB.get_current()


class Accesses(Command):
    async def start(self):
        builder = ["{uid}: {name} – ({code})".format(
            uid=command.uid, name=command.name,
            code=db.accesses[self.message.chat_id][command.uid]
        ) for command in Manager.commands
        ]
        return "Доступы команд:\n{}".format("\n".join(builder))