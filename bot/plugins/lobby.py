from typing import List

from datetime import datetime

import httpx

from bot.schedule import schedule
from bot.settings import KELEI_TOKEN
from bot.command import CommandRouter


class LobbyRoomCache:
    def __init__(self) -> None:
        self._cache = {}
        self.lobby_room_key = "lobby_room"

    def set(self, rooms: List[dict]):
        update_at = datetime.now()
        self._cache[self.lobby_room_key] = {
            "data": rooms,
            "update_at": update_at.strftime("%Y-%m-%d-%H:%M:%S"),
        }


router = CommandRouter()
cache = LobbyRoomCache()


async def read_room_details(
    row_id: str,
    region: str,
) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"https://lobby-v2-{region}.klei.com/lobby/read"
        payload = {
            "__token": KELEI_TOKEN,
            "__gameId": "DST",
            "query": {"__rowId": row_id},
        }
        return await client.post(url, json=payload)


async def read_lobby_room(
    region: str,
) -> List[dict]:
    url = f"https://lobby-v2-cdn.klei.com/{region}-Steam.json.gz"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()["GET"]


async def read_regions() -> List[str]:
    async with httpx.AsyncClient() as client:
        url = "https://lobby-v2-cdn.klei.com/regioncapabilities-v2.json"
        response = await client.get(url)
    return [item["Region"] for item in response.json()["LobbyRegions"]]


@schedule.job(minutes=30)
async def update_lobby_room():
    rooms = []
    for region in await read_regions():
        region_rooms = await read_lobby_room(region)
        rooms.extend(region_rooms)
    # 缓存到全局变量里
    global cache
    cache.set(rooms)
