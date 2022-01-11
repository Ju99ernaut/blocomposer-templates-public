import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Comment, User, Message, Count
from dependencies import get_user
from utils.tasks import add_author

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/count", response_model=Count)
async def read_count(user: User = Depends(get_user)):
    return {"count": data.get_user_comments_count(user["id"])}


@router.get("/{uuid}", response_model=Comment)
async def read_comment_with_id(uuid: UUID, user: User = Depends(get_user)):
    comment = data.get_comment(uuid, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.get("/template/{template}", response_model=List[Comment])
async def get_comments(
    template: UUID,
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [
        add_author(comment)
        for comment in data.get_all_template_comments(template, page, size)
    ]


@router.post("", response_model=Comment)
async def add_comment(comment: Comment, user: User = Depends(get_user)):
    comment.author = user["id"]
    data.add_comment(comment.dict())
    comment = data.get_comment(comment.id, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.patch("/{uuid}", response_model=Comment)
async def update_comment(uuid: UUID, comment: Comment, user: User = Depends(get_user)):
    comment.id = uuid
    data.update_comment(comment.dict())
    comment = data.get_comment(uuid, user["id"])
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/{uuid}", response_model=Message)
async def delete_comment_with_id(uuid: UUID, user: User = Depends(get_user)):
    data.remove_comment(uuid, user["id"])
    if data.get_comment(uuid, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}