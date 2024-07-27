import structlog
from fastapi import APIRouter, Body, Query

from bot import models


router = APIRouter()
log = structlog.get_logger()


@router.post("")
async def create(
    uid: str = Body(embed=True, description="QQ号"),
):
    return await models.Admin.create(uid=uid)


@router.delete("")
async def remove(
    uid: str = Query(),
):
    return await models.Admin.filter(uid=uid).delete()
