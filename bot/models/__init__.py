from tortoise import models, fields


class Admin(models.Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(unique=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
