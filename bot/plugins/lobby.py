from typing import List, Literal, Dict, Any

import re
import asyncio
from datetime import datetime

import httpx
import structlog

from bot.schemas import Event
from bot.schedule import schedule
from bot.settings import KELEI_TOKEN
from bot.command import CommandRouter


log = structlog.get_logger()


class LobbyRoomCache:
    def __init__(self) -> None:
        self._cache = {}

    def set(
        self,
        key: Literal["lobby_room", "room_details", "history_room"],
        data,
    ):
        self._cache[key] = {
            "data": data,
            "update_at": datetime.now().strftime("%Y-%m-%d-%H:%M"),
        }

    def get(
        self,
        key: Literal["lobby_room", "room_details", "history_room"],
    ) -> Dict[str, Any]:
        return self._cache.get(key)


global cache
router = CommandRouter()
cache = LobbyRoomCache()


async def read_room_details(
    row_id: str,
    region: str,
) -> dict:
    room_details = {}
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://lobby-v2-{region}.klei.com/lobby/read"
            payload = {
                "__token": KELEI_TOKEN,
                "__gameId": "DST",
                "query": {"__rowId": row_id},
            }
            response = await client.post(url, json=payload)
            room_details = response.json()["GET"][0]
            room_details["region"] = region
    except Exception as e:
        log.exception(f"[read_room_details] error: {e}")
    return room_details


async def read_lobby_room(
    region: str,
) -> List[dict]:
    url = f"https://lobby-v2-cdn.klei.com/{region}-Steam.json.gz"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    rooms = []
    for item in response.json()["GET"]:
        item["region"] = region
        rooms.append(item)
    return rooms


async def read_regions() -> List[str]:
    async with httpx.AsyncClient() as client:
        url = "https://lobby-v2-cdn.klei.com/regioncapabilities-v2.json"
        response = await client.get(url)
    return [item["Region"] for item in response.json()["LobbyRegions"]]


@schedule.job(minutes=15)
async def update_lobby_room():
    log.info("[update_lobby_room]")
    rooms = []
    for region in await read_regions():
        region_rooms = await read_lobby_room(region)
        rooms.extend(region_rooms)
    global cache
    cache.set("lobby_room", rooms)


@schedule.job(hours=1)
async def update_room_details():
    log.info("[update_room_details]")
    rooms = []
    tasks = []
    for region in await read_regions():
        for room in await read_lobby_room(region):
            tasks.append(read_room_details(room["__rowId"], region))
    split_tasks = [[]]
    while tasks:
        if len(split_tasks[-1]) < 12:
            split_tasks[-1].append(tasks.pop())
        else:
            split_tasks.append([tasks.pop()])
    for tasks in split_tasks:
        result = await asyncio.gather(*tasks)
        for room_details in result:
            if "__rowId" in room_details:
                rooms.append(room_details)
    cache.set("room_details", rooms)


@router.command("查服.*+")
async def find_lobby_room(event: Event):
    key = event.match_text.removeprefix("查服").strip()
    reply_message = "服务器如下: \n\n"
    if cache.get("lobby_room") is None:
        await update_lobby_room()
    count = 0
    history_room = {}
    lobby_room = cache.get("lobby_room")
    for room in lobby_room["data"]:
        name = room["name"]
        if key in name:
            count += 1
            history_room[count] = {
                "row_id": room["__rowId"],
                "region": room["region"],
            }
            reply_message += f'{count}.{name} 在线人数: {room["connected"]}\n'
        if count >= 10:
            break
    reply_message += f'数据更新时间: {lobby_room["update_at"]}'
    cache.set("history_room", history_room)
    return reply_message


@router.command("查玩家.*+")
async def find_player_in_room(event: Event):
    key = event.match_text.removeprefix("查玩家").strip()
    count = 0
    history_room = {}
    reply_message = "服务器如下: \n\n"
    room_details = cache.get("room_details")
    if room_details is None:
        return "数据更新..."
    for room in room_details["data"]:
        name = room["name"]
        players = re.findall(r'name="(.*?)"', room["players"])
        day = re.findall(r"day=([0-9]+)", room["data"])
        day = day[0] if day else "未知"
        season = room["season"]
        for player in players:
            if key in player:
                count += 1
                history_room[count] = {
                    "row_id": room["__rowId"],
                    "region": room["region"],
                }
                reply_message += f'{count}.{name} 玩家: {player} 在线人数: {room["connected"]} 天数: {day} 季节: {season} \n'
        if count >= 10:
            break
    reply_message += f'数据更新时间: {room_details["update_at"]}'
    cache.set("history_room", history_room)
    return reply_message


@router.command("查房间.*+")
async def find_room_details(event: Event):
    key = event.match_text.removeprefix("查房间").strip()
    try:
        room = cache.get("history_room")["data"][int(key)]
        room_details = await read_room_details(room["row_id"], room["region"])
        # 解析
        name = room["name"]
        desc = room["desc"]
        season = room["season"]
        player_desc = ""
        players = re.findall(r'name="(.*?)"', room_details["players"])
        for player in players[:32]:
            player_desc += player + "\n"
        if len(players) > 32:
            player_desc += "..." + "\n"
        day = re.findall(r"day=([0-9]+)", room_details["data"])
        day = day[0] if day else "未知"
        c_connect = f"""c_connect("{room_details['__addr']}", {room_details['port']})"""
        # 拼接消息
        reply_message = f"存档: {name}\n"
        reply_message += f"玩家: {player_desc}\n"
        reply_message += f"天数: {day}\n"
        reply_message += f"季节: {season}\n"
        reply_message += f"直连: {c_connect}\n"
        reply_message += f"介绍: {desc}\n"
        return reply_message
    except Exception:
        return None
