import httpx

from bot import models
from bot.command import CommandRouter


router = CommandRouter()


@router.command("ls", inject_event=False)
async def ls():
    reply_message = ""
    async with httpx.AsyncClient() as client:
        async for dst_server in models.DSTServer.all():
            url = f"{dst_server.endpoint}/deploy/{dst_server.cluster_id}"
            response = await client.get(url)
            # 解析获取存档名
            cluster = response.json()
            if cluster["status"] != "running":
                continue
            reply_message += cluster["content"]["ini"]["cluster_name"] + ","
    return reply_message
