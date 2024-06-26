from tortoise import models, fields


class DSTServer(models.Model):
    id = fields.IntField(pk=True)
    cluster_id = fields.IntField()
    name = fields.CharField(max_length=256, unique=True)
    endpoint = fields.CharField(max_length=256)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Admin(models.Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(unique=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
