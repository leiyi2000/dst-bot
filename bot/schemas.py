from typing import Literal, List

from pydantic import BaseModel

from bot.settings import BOT_ACCOUNT


class FileMessage(BaseModel):
    file: str
    name: str


class TextMessage(BaseModel):
    text: str


class ImageMessage(BaseModel):
    file: str
    url: str
    file_size: str


class Message(BaseModel):
    type: Literal["file", "text", "image"]
    data: FileMessage | TextMessage | ImageMessage


class NodeMessage(BaseModel):
    name: str = "wendy"
    uin: str = BOT_ACCOUNT
    content: str


class Event(BaseModel):
    user_id: int | None = None
    group_id: int | None = None
    message_type: Literal["private", "group"]
    message: List[Message]
    time: int
    # 匹配上的指令消息
    match_text: str | None = None
