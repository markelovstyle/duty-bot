from enum import Enum, IntEnum


class Mode(Enum):
    ONLY_CHAT = "only_chat"
    ONLY_USER = "only_user"
    ALL = "all"