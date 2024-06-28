import httpx

from bot import models
from bot.command import CommandRouter


router = CommandRouter()


@router.command("服务器列表", inject_event=False)
async def ls():
    reply_message = "群服务器如下: \n"
    async with httpx.AsyncClient() as client:
        async for dst_server in models.DSTServer.all():
            url = f"{dst_server.endpoint}/deploy/{dst_server.cluster_id}"
            response = await client.get(url)
            # 解析获取存档名
            cluster = response.json()
            if cluster["status"] != "running":
                continue
            status = "运行" if cluster["status"] != "running" else "停止"
            line = f'{cluster["content"]["ini"]["cluster_name"]} {status}\n'
            reply_message += line
    return reply_message
