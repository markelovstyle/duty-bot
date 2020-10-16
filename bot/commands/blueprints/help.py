from ..abc import Command


class Help(Command):
    async def start(self):
        return "Список команд ещё недоступен."