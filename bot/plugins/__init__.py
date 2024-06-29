from bot.command import CommandRouter
from bot.plugins import cluster, helper, lobby


# 指令注入
router = CommandRouter()
router.include_router(helper.router)
router.include_router(cluster.router)
router.include_router(lobby.router)
