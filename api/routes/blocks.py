import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from models import Block, User, Message
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


@router.get("/{id}", response_model=Block)
async def read_block_with_id(id: UUID, user: User = Depends(get_user)):
    block = data.get_block(id, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.post("", response_model=Block)
async def add_block(id: UUID, block: Block, user: User = Depends(get_user)):
    data.add_block(block.dict())
    block = data.get_block(id, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.patch("/{id}", response_model=Block)
async def update_block(id: UUID, block: Block, user: User = Depends(get_user)):
    data.update_block(block.dict())
    block = data.get_block(id, user["id"])
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.delete("/{id}", response_model=Message)
async def delete_block_with_id(id: UUID, user: User = Depends(get_user)):
    data.remove_block(id, user["id"])
    if data.remove_block(id, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Failed to delete"
        )
    return {"msg": "success"}