import httpx

from bot.settings import WENDY_API
from bot.command import CommandRouter
from bot.schemas import Event, NodeMessage


router = CommandRouter()


@router.command("ls", inject_event=False)
async def ls():
    cluster_id = ""
    reply_message = "本群服务器如下: \n\n"
    async with httpx.AsyncClient() as client:
        url = f"{WENDY_API}/deploy?status=running"
        response = await client.get(url)
        for cluster in response.json():
            cluster_id = cluster["id"]
            cluster_name = cluster["cluster"]["ini"]["cluster_name"]
            reply_message += f"{cluster_id}. {cluster_name}\n"
    if cluster_id:
        reply_message += f"\n发送备份指令即可备份存至群文件如: 备份{cluster_id}\n"
        reply_message += "注意: 备份存档会引起游戏卡顿"
        return [NodeMessage(content=reply_message)]
    else:
        "404~~"


@router.command("重启.*+", limit_admin=True)
async def restart(event: Event):
    id = event.match_text.removeprefix("重启").strip()
    async with httpx.AsyncClient(timeout=300) as client:
        url = f"{WENDY_API}/deploy/restart/{id}"
        await client.get(url)
    return "重启中"


@router.command("关服.*+", limit_admin=True)
async def stop(event: Event):
    id = event.match_text.removeprefix("关服").strip()
    async with httpx.AsyncClient(timeout=300) as client:
        url = f"{WENDY_API}/deploy/stop/{id}"
        await client.get(url)
    return "关闭中"
