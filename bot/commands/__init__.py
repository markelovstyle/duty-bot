from .manager import register_command
from .blueprints.help import Help
from .blueprints.accesses import Accesses


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