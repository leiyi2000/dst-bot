"""消息事件"""

import structlog
from fastapi import APIRouter, Body, BackgroundTasks

from bot import models
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
        # 对于文件类型的event入库
        for item in event.message:
            if item.type == "file":
                # 文件类型数据准备入库
                await models.FileEvent.create(
                    file=item.data.file,
                    file_id=item.data.file_id,
                )
        background_tasks.add_task(run_command, plugin_router, event)
    except Exception:
        # log.exception(f"new type message: {message} error: {e}")
        pass
    return "ok"
