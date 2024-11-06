from tortoise import models, fields


class Admin(models.Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(unique=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class FileEvent(models.Model):
    id = fields.IntField(pk=True)
    file = fields.CharField(max_length=128, description="文件名")
    file_id = fields.CharField(max_length=512, description="文件ID")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
