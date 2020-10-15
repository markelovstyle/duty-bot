from typing import List
from vkbottle.user import Blueprint

bp = Blueprint()


async def get_users(ids: List[int]):
    return await bp.api.users.get(
        user_ids=ids
    )


async def get_chat_data(chat_id: int) -> tuple:
    response = await bp.api.request("messages.getChat", {
        "chat_id": chat_id
    })
    return (
        response["title"],
        response["admin_id"],
        response["users"]
    )