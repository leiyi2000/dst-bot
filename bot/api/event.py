"""消息事件"""

import json

import structlog
from fastapi import APIRouter, Body, BackgroundTasks


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
    return "ok"
