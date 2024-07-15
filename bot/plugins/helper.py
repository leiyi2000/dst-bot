import httpx

from bot import models
from bot.schemas import NodeMessage
from bot.settings import BOT_ACCOUNT
from bot.command import CommandRouter


router = CommandRouter()


@router.command("ls", inject_event=False)
async def ls():
    room_short = ""
    reply_message = "本群服务器如下: \n\n"
    async with httpx.AsyncClient() as client:
        async for dst_server in models.DSTServer.all():
            url = f"{dst_server.endpoint}/deploy/{dst_server.cluster_id}"
            response = await client.get(url)
            cluster = response.json()
            room_short = dst_server.name
            status = "运行" if cluster["status"] == "running" else "停止"
            reply_message += f'存档: {cluster["content"]["ini"]["cluster_name"]}\n'
            reply_message += f"简称: {room_short}\n"
            reply_message += f"状态: {status}\n\n"
    if room_short:
        reply_message += f"发送备份指令即可备份存至群文件如: 备份{room_short}\n"
        reply_message += "注意: 备份存档会引起游戏卡顿"
        return [NodeMessage(name="wendy", uin=BOT_ACCOUNT, content=reply_message)]
    else:
        "什么也没有"
