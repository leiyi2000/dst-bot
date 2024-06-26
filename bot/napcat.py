from typing import Literal

import httpx
import structlog

from bot.schemas import Message
from bot.settings import NAPCAT_API


log = structlog.get_logger()


async def download_file(url: str):
    """下载文件.

    Args:
        url (str): 文件下载地址.
        filename (str): 文件名.
        user_id (int | None): QQ.
        group_id (int | None): 群号.
        message_type (Literal["private", "group"]): 消息类型.
    """
    async with httpx.AsyncClient() as client:
        payload = {"url": url}
        response = await client.post(
            f"{NAPCAT_API}/download_file", json=payload, timeout=600
        )
        return f'file://{response.json()["data"]["file"]}'


async def send_message(
    message: str | dict | Message,
    user_id: int | None = None,
    group_id: int | None = None,
    message_type: Literal["private", "group"] = "group",
) -> dict:
    """发送消息.

    Args:
        message (str | dict | Message): 消息.
        user_id (int | None): QQ.
        group_id (int | None): 群号.
        message_type (Literal["private", "group"]): 消息类型.
    """
    if isinstance(message, str):
        message = {
            "type": "text",
            "data": {
                "text": message,
            },
        }
    elif isinstance(message, Message):
        message = message.model_dump(mode="json")
    async with httpx.AsyncClient() as client:
        payload = {
            "message_type": message_type,
            "user_id": user_id,
            "group_id": group_id,
            "message": message,
        }
        log.info(f"[send_message]: {payload}")
        response = await client.post(
            f"{NAPCAT_API}/send_msg",
            json=payload,
            timeout=600,
        )
    return response.json()
