from enum import Enum, IntEnum


class Accessibility(Enum):
    ONLY_CHAT = "only_chat"
    ONLY_USER = "only_user"
    ALL = "all"


class Sender(IntEnum):
    FROM_CHAT = 0
    FROM_USER = 1