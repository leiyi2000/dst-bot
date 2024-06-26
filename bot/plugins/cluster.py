from datetime import datetime

from bot import napcat, models
from bot.command import CommandRouter
from bot.schemas import Event, Message, FileMessage


router = CommandRouter()


@router.command("备份*")
async def backup(event: Event):
    name = event.match_text.removeprefix("备份").strip()
    dst_server = await models.DSTServer.filter(name=name).first()
    if not dst_server:
        return "备份失败，请输入正确的服务器名称"
    name = f"{name}-{datetime.now().strftime('%Y%m%d%H%M')}.zip"
    file_url = f"{dst_server.endpoint}/cluster/download/{dst_server.cluster_id}"
    file = await napcat.download_file(file_url)
    return Message(
        type="file",
        data=FileMessage(file=file, name=name),
    )
