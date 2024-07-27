"""路由配置"""

from fastapi import APIRouter

from bot.api import event, admin


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(
    event.router,
    prefix="/event",
    tags=["事件上报"],
)


router.include_router(
    admin.router,
    prefix="/admin",
    tags=["管理"],
)
