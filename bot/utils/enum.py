from enum import Enum


class TaskType(Enum):
    DISPOSABLE = "disposable"
    PERIODIC = "periodic"


class Mode(Enum):
    ONLY_CHAT = "only_chat"
    ONLY_USER = "only_user"
    ALL = "all"