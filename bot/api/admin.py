import structlog
from fastapi import APIRouter, Body, Query

from bot import models


router = APIRouter()
log = structlog.get_logger()


@router.post("")
async def create(
    uid: str = Body(embed=True, description="QQ号"),
):
    admin = await models.Admin.get_or_none(uid=uid)
    if admin is None:
        return await models.Admin.create(uid=uid)
    else:
        return admin


@router.delete("")
async def remove(
    uid: str = Query(),
):
    return await models.Admin.filter(uid=uid).delete()
