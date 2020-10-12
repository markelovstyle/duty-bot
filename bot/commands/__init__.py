from .manager import register_command
from .blueprints.hello import Hello


async def include_commands():
    await register_command(
        name="Привет",
        description="Отвечает пользователю на приветствие",
        handler=Hello,
        accessibility="all",
        patterns=["привет"]
    )