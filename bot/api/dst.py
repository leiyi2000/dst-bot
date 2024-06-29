from fastapi import APIRouter, Body

from bot import models


router = APIRouter()


@router.post(
    "",
    description="注入一个DST服",
)
async def create(
    name: str = Body(),
    endpoint: str = Body(),
    cluster_id: int = Body(),
):
    dst_server = await models.DSTServer.create(
        name=name,
        endpoint=endpoint,
        cluster_id=cluster_id,
    )
    return dst_server


@router.get(
    "",
    description="获取所有DST服",
)
async def reads():
    return await models.DSTServer.all()


@router.delete(
    "/{id}",
    description="删除一个DST服",
)
async def delete(id: int):
    return await models.DSTServer.delete(id)


@router.put(
    "/{id}",
    description="更新一个DST服",
)
async def update(
    id: int,
    name: str = Body(),
    endpoint: str = Body(),
    cluster_id: int = Body(),
):
    return await models.DSTServer.filter(id=id).update(
        name=name,
        endpoint=endpoint,
        cluster_id=cluster_id,
    )
