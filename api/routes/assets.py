import os
import data
import requests

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Asset, User, Message, Count
from dependencies import get_user
from utils.tasks import add_author

router = APIRouter(
    prefix="/assets", tags=["assets"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[Asset])
async def read_assets(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [asset for asset in data.get_all_assets(user["id"], page, size)]


@router.get("/expand", response_model=List[Asset])
async def read_assets(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    author = data.get_author(user["id"])
    return [
        add_author(asset, author)
        for asset in data.get_all_assets(user["id"], page, size)
    ]


@router.get("/count", response_model=Count)
async def read_count(user: User = Depends(get_user)):
    return {"count": data.get_user_assets_count(user["id"])}


@router.get("/{uid}", response_model=Asset)
async def read_asset(uid: str, user: User = Depends(get_user)):
    asset = data.get_asset(uid, user["id"])
    if not asset:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset


@router.post("", response_model=Asset)
async def add_asset(asset: Asset, user: User = Depends(get_user)):
    count = data.get_user_assets_count(user["id"])
    if count < 25:
        asset.author = user["id"]
        data.add_asset(asset.dict())
    asset_db = data.get_asset(asset.uid, user["id"])
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset_db


@router.patch("/{uid}", response_model=Asset)
async def update_asset(uid: str, asset: Asset, user: User = Depends(get_user)):
    asset.uid = uid
    data.update_asset(asset.dict())
    asset_db = data.get_asset(asset.uid, user["id"])
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset_db


@router.delete("/{uid}", response_model=Message)
async def delete_asset(uid: str, user: User = Depends(get_user)):
    url = os.getenv("TUS_ENDPOINT") + uid
    result = requests.delete(url, headers={"Tus-Resumable": "1.0.0"})
    code = result.status_code
    if not (code == 204 or code == 404 or code == 410):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to delete file",
        )
    else:
        data.remove_asset(uid, user["id"])
        if data.get_asset(uid, user["id"]):
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="Failed to delete reference",
            )
        return {"msg": "success"}