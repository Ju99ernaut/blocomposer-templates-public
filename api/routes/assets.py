import data

from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Asset, User, Message
from dependencies import get_user
from utils.tasks import  add_author

router = APIRouter(
    prefix="/assets", tags=["assets"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[Asset])
async def read_assets(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    author = data.get_author(user["id"])
    return [add_author(asset, author) for asset in data.get_all_assets(user["id"], page, size)]


@router.get("/{uuid}", response_model=Asset)
async def read_asset(uuid: UUID, user: User = Depends(get_user)):
    asset = data.get_asset(uuid, user["id"])
    if not asset:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_author(asset)


@router.post("", response_model=Asset)
async def add_asset(asset: Asset, user: User = Depends(get_user)):
    asset.author = user["id"]
    data.add_asset(asset.dict())
    asset_db = data.get_asset(asset.id, user["id"])
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_author(asset_db)


@router.patch("/{uuid}", response_model=Asset)
async def update_asset(uuid: UUID, asset: Asset, user: User = Depends(get_user)):
    asset.id = uuid
    data.update_asset(asset.dict())
    asset_db = data.get_asset(asset.id, user["id"])
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return add_author(asset_db)


@router.delete("/{uuid}", response_model=Message)
async def delete_asset(uuid: UUID, user: User = Depends(get_user)):
    data.remove_asset(uuid, user["id"])
    if data.get_asset(uuid, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}