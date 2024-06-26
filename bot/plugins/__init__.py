from bot.command import CommandRouter
from bot.plugins import cluster, dst


# 指令注入
router = CommandRouter()
router.include_router(dst.router)
router.include_router(cluster.router)
