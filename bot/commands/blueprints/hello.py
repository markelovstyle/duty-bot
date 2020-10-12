from ..abc import Command


class Hello(Command):
    async def start(self):
        return "Привет!"