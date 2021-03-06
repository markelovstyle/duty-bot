from tortoise import fields, Model
from ..utils.display import display_ranks

__all__ = (
    "Commands",
    "Chat",
    "Members",
    "Users",
    "Ranks"
)


class Commands(Model):
    id = fields.SmallIntField(pk=True)
    name = fields.CharField(max_length=150)
    type = fields.CharField(max_length=9)
    description = fields.TextField(null=True)
    access_code = fields.SmallIntField()


class Chat(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=450)
    owner_id = fields.IntField()
    accesses = fields.JSONField()

    def load_model(self) -> dict:
        copy = self.accesses.copy()
        self.accesses.clear()
        self.accesses.update({int(k): int(v) for k, v in copy.items()})
        return {self.id: self.accesses}


class Members(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    chat_id = fields.IntField()
    rank = fields.SmallIntField(default=0)
    left = fields.BooleanField(default=False)


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def load_model(self) -> dict:
        return {self.id: self.name}


class Ranks(Model):
    id = fields.IntField(pk=True)
    tags = fields.JSONField(default=display_ranks)

    def load_model(self) -> dict:
        copy = self.tags.copy()
        self.tags.clear()
        self.tags.update({int(k): v for k, v in copy.items()})
        return {self.id: self.tags}
