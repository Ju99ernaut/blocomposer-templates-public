import data

from typing import List

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from models import Block

router = APIRouter(
    prefix="/blocks",
    tags=["blocks"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Block])
async def read_blocks():
    return [block for block in data.get_all_blocks()]


@router.get("/{id}", response_model=Block)
async def read_block_with_id(id: UUID):
    block = data.get_block(id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.post("/{id}", response_model=Block)
async def add_block(id: UUID, block: Block):
    data.add_block(block.dict())
    block = data.get_block(id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.patch("/{id}", response_model=Block)
async def update_block(id: UUID, block: Block):
    data.add_block(block.dict())
    block = data.get_block(id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.delete(
    "/{id}",
    response_model=List[Block],
)
async def delete_block_with_id(id: UUID):
    data.remove_block(id)
    return [block for block in data.get_all_blocks()]