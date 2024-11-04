"""消息事件"""

import structlog
from fastapi import APIRouter, Body, BackgroundTasks

from bot.schemas import Event
from bot.command import run_command
from bot.plugins import router as plugin_router

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
    try:
        event = Event.model_validate(message)
        log.info(f"event: {event}")
        background_tasks.add_task(run_command, plugin_router, event)
    except Exception:
        # log.exception(f"new type message: {message} error: {e}")
        pass
    return "ok"
