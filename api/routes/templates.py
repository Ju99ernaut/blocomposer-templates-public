import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Template, User, Message
from utils.tasks import prefix, add_author
from dependencies import get_user

router = APIRouter(
    prefix="/templates",
    tags=["templates"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[Template])
async def read_templates(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    author = data.get_author(user["id"])
    return [
        add_author(prefix(template), author)
        for template in data.get_all_templates(user["id"], page, size)
    ]


@router.get("/public", response_model=List[Template])
async def read_puplic_templates(
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [
        add_author(prefix(template))
        for template in data.get_all_public_templates(page, size)
    ]


@router.get("/{uuid}", response_model=Template)
async def read_template_with_id(uuid: UUID):
    template = data.get_template(uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return add_author(prefix(template))


@router.post("/{uuid}", response_model=Template)
async def add_template(uuid: UUID, template: Template, user: User = Depends(get_user)):
    data.add_template(template.dict())
    template = data.get_template(uuid, user["id"])
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return add_author(prefix(template))


@router.delete("/{uuid}", response_model=Message)
async def delete_template_with_id(uuid: UUID, user: User = Depends(get_user)):
    data.remove_template(uuid, user["id"])
    if data.get_template(uuid, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}