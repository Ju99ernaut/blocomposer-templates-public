import data

from typing import List

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from models import Bookmark

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Bookmark])
async def read_bookmarks():
    return [bookmark for bookmark in data.get_all_bookmarks()]


@router.get("/{id}", response_model=Bookmark)
async def read_template_with_id(id: UUID):
    bookmark = data.get_bookmark(id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.post("/{id}", response_model=Bookmark)
async def add_template(id: UUID, bookmark: Bookmark):
    data.add_bookmark(bookmark.dict())
    bookmark = data.get_bookmark(id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.patch("/{id}", response_model=Bookmark)
async def update_template(id: UUID, bookmark: Bookmark):
    data.add_bookmark(bookmark.dict())
    bookmark = data.get_bookmark(id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.delete(
    "/{id}",
    response_model=List[Bookmark],
)
async def delete_bookmark_with_id(id: UUID):
    data.remove_bookmark(id)
    return [bookmark for bookmark in data.get_all_bookmarks()]