from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "fileevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "file" VARCHAR(128) NOT NULL  /* 文件名 */,
    "file_id" VARCHAR(512) NOT NULL  /* 文件ID */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "fileevent";"""
