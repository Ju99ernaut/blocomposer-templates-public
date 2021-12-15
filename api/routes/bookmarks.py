import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Bookmark, BookmarkRef, User, Message
from dependencies import get_user

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[BookmarkRef])
async def read_bookmarks(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [bookmark for bookmark in data.get_all_bookmarks(user["id"], page, size)]


@router.get("/{uuid}", response_model=BookmarkRef)
async def read_template_with_id(uuid: UUID, user: User = Depends(get_user)):
    bookmark = data.get_bookmark(uuid, user["id"])
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.post("", response_model=BookmarkRef)
async def add_template(uuid: UUID, bookmark: Bookmark, user: User = Depends(get_user)):
    data.add_bookmark(bookmark.dict())
    bookmark = data.get_bookmark(uuid, user["id"])
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.patch("/{uuid}", response_model=BookmarkRef)
async def update_template(
    uuid: UUID, bookmark: Bookmark, user: User = Depends(get_user)
):
    data.update_bookmark(bookmark.dict())
    bookmark = data.get_bookmark(uuid, user["id"])
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.delete("/{uuid}", response_model=Message)
async def delete_bookmark_with_id(uuid: UUID, user: User = Depends(get_user)):
    data.remove_bookmark(uuid, user["id"])
    if data.get_bookmark(uuid, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}