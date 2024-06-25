from datetime import datetime

from bot import napcat
from bot.schemas import Message, FileMessage
from bot.command import CommandRouter


router = CommandRouter()


@router.command("蜘蛛备份", inject_event=False)
async def backup():
    name = f"蜘蛛-{datetime.now().strftime('%Y%m%d%H%M')}.zip"
    file = await napcat.download_file("http://113.31.186.221:8000/cluster/download/3")
    return Message(
        type="file",
        data=FileMessage(file=file, name=name),
    )
