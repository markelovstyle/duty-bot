from ..abc import Command
from ..manager import Manager


class Help(Command):
    async def start(self):
        commands = [
            "{uid}: {name}".format(uid=command.uid, name=command.name)
            for command in Manager.commands
        ]
        return "Список команд:\n{}".format("\n".join(commands))