import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from models import Comment, CommentRef, User, Message
from dependencies import get_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{template}", response_model=List[CommentRef])
async def get_comments(
    template: UUID,
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [bookmark for bookmark in data.get_all_comments(template, page, size)]


@router.get("/{id}", response_model=CommentRef)
async def read_comment_with_id(id: UUID, user: User = Depends(get_user)):
    comment = data.get_comment(id, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("", response_model=CommentRef)
async def add_comment(id: UUID, comment: Comment, user: User = Depends(get_user)):
    data.add_comment(comment.dict())
    comment = data.get_comment(id, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.patch("/{id}", response_model=CommentRef)
async def update_comment(id: UUID, comment: Comment, user: User = Depends(get_user)):
    data.add_comment(comment.dict())
    comment = data.get_comment(id, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/{id}", response_model=Message)
async def delete_comment_with_id(id: UUID, user: User = Depends(get_user)):
    data.remove_comment(id, user["id"])
    if data.remove_comment(id, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}