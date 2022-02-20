import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Block, User, Message, Count
from dependencies import get_user

router = APIRouter(
    prefix="/blocks",
    tags=["blocks"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Block])
async def read_blocks(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [block for block in data.get_all_blocks(user["id"], page, size)]


@router.get("/count", response_model=Count)
async def read_count(user: User = Depends(get_user)):
    return {"count": data.get_user_blocks_count(user["id"])}


@router.get("/{uuid}", response_model=Block)
async def read_block_with_id(uuid: UUID, user: User = Depends(get_user)):
    block = data.get_block(uuid, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.post("", response_model=Block)
async def add_block(block: Block, user: User = Depends(get_user)):
    count = data.get_user_assets_count(user["id"])
    if count < 10:
        block.author = user["id"]
        data.add_block(block.dict())
    block = data.get_block(block.uuid, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.patch("/{uuid}", response_model=Block)
async def update_block(uuid: UUID, block: Block, user: User = Depends(get_user)):
    block.uuid = uuid
    data.update_block(block.dict())
    block = data.get_block(uuid, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.delete("/{uuid}", response_model=Message)
async def delete_block_with_id(uuid: UUID, user: User = Depends(get_user)):
    data.remove_block(uuid, user["id"])
    if data.get_block(uuid, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}