from bot.command import CommandRouter
from bot.plugins import cluster


# 指令注入
router = CommandRouter()
router.include_router(cluster.router)
