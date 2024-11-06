from datetime import datetime

import httpx

from bot import napcat
from bot.settings import WENDY_API
from bot.command import CommandRouter
from bot.schemas import Event, Message, FileMessage


router = CommandRouter()


@router.command("备份.*+")
async def backup(event: Event):
    id = event.match_message.removeprefix("备份").strip()
    async with httpx.AsyncClient() as client:
        url = f"{WENDY_API}/deploy/{id}"
        response = await client.get(url)
        cluster = response.json()
        cluster_name = cluster["cluster"]["ini"]["cluster_name"]
    file = await napcat.download_file(f"{WENDY_API}/cluster/download/{id}")
    filename = f"{cluster_name[:6]}-{datetime.now().strftime('%Y%m%d%H')}.tar"
    file_message = FileMessage(file=file, name=filename)
    return Message(
        type="file",
        data=file_message,
    )
