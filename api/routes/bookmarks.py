import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Bookmark, User, Message
from dependencies import get_user
from constants import TEMPLATE_KEY, AUTHOR_KEY

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"],
    responses={404: {"description": "Not found"}},
)


def expand(dictionary):
    dictionary[TEMPLATE_KEY] = data.get_template(dictionary[TEMPLATE_KEY])
    dictionary[TEMPLATE_KEY][AUTHOR_KEY] = data.get_author(
        dictionary[TEMPLATE_KEY][AUTHOR_KEY]
    )
    return dictionary


@router.get("", response_model=List[Bookmark])
async def read_bookmarks(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [bookmark for bookmark in data.get_all_bookmarks(user["id"], page, size)]


@router.get("/expand", response_model=List[Bookmark])
async def read_bookmarks(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [
        expand(bookmark) for bookmark in data.get_all_bookmarks(user["id"], page, size)
    ]


@router.get("/{uuid}", response_model=Bookmark)
async def read_bookmark_with_id(uuid: UUID, user: User = Depends(get_user)):
    bookmark = data.get_bookmark(uuid, user["id"])
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.post("", response_model=Bookmark)
async def add_bookmark(bookmark: Bookmark, user: User = Depends(get_user)):
    bookmark.author = user["id"]
    data.add_bookmark(bookmark.dict())
    bookmark = data.get_bookmark(bookmark.id, user["id"])
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.patch("/{uuid}", response_model=Bookmark)
async def update_bookmarks(
    uuid: UUID, bookmark: Bookmark, user: User = Depends(get_user)
):
    bookmark.id = uuid
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