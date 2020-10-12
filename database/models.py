from tortoise import fields, Model


class Commands(Model):
    id = fields.SmallIntField(pk=True)
    name = fields.CharField(max_length=150)
    type = fields.CharField(max_length=9)
    description = fields.TextField(null=True)


