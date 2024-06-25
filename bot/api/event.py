"""消息事件"""

import json

import structlog
from fastapi import APIRouter, Body, BackgroundTasks

from bot.schemas import Event


router = APIRouter()
log = structlog.get_logger()


@router.post(
    "",
    description="消息上报",
)
async def receive(
    background_tasks: BackgroundTasks,
    message: dict = Body(),
):
    log.info(f"message: {json.dumps(message, indent=4, ensure_ascii=False)}")
    event = Event.model_validate(message)
    log.info(f"event: {event.model_dump_json(indent=4)}")
    return "ok"
