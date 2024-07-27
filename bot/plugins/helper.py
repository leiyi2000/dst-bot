import httpx

from bot.settings import WENDY_API
from bot.schemas import NodeMessage
from bot.command import CommandRouter


router = CommandRouter()


@router.command("ls", inject_event=False)
async def ls():
    room_short = ""
    reply_message = "本群服务器如下: \n\n"
    async with httpx.AsyncClient() as client:
        url = f"{WENDY_API}/deploy?status=running"
        response = await client.get(url)
        for cluster in response.json():
            room_short = cluster["id"]
            reply_message += f"ID: {room_short}\n"
            reply_message += f'存档: {cluster["content"]["ini"]["cluster_name"]}\n'
    if room_short:
        reply_message += f"发送备份指令即可备份存至群文件如: 备份{room_short}\n"
        reply_message += "注意: 备份存档会引起游戏卡顿"
        return [NodeMessage(content=reply_message)]
    else:
        "404~~"
