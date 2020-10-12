from .manager import register_command
from .blueprints.hello import Hello
from .blueprints.help import Help


async def include_commands():
    await register_command(
        name="Привет",
        description="Отвечает пользователю на приветствие",
        handler=Hello,
        accessibility="all",
        patterns=["привет"]
    )
    await register_command(
        name="Помощь",
        description="Навигация по всему функционалу бота",
        handler=Help,
        accessibility="all",
        patterns=["помощь", "команды"]
    )