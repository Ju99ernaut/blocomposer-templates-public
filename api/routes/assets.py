import data

from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models import Asset

router = APIRouter(
    prefix="/assets", tags=["assets"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[Asset])
async def read_assets():
    return [asset for asset in data.get_all_assets()]


@router.get("/{id}", response_model=Asset)
async def read_asset(id: UUID):
    asset = data.get_asset(id)
    if not asset:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset


@router.post("", response_model=Asset)
async def add_asset(asset: Asset):
    data.add_item(asset.dict())
    asset_db = data.get_asset(asset.id)
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset_db


@router.patch("", response_model=Asset)
async def update_asset(asset: Asset):
    data.add_item(asset.dict())
    asset_db = data.get_asset(asset.id)
    if not asset_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return asset_db


@router.delete(
    "",
    response_model=List[Asset],
)
async def delete_asset(id: UUID):
    data.remove_asset(id)
    return [asset for asset in data.get_all_assets()]