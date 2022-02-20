import data

from typing import List, Optional

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Template, TemplateId, User, Message, Count
from utils.tasks import prefix, add_author
from dependencies import get_user

router = APIRouter(
    prefix="/templates",
    tags=["templates"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[TemplateId])
async def read_user_templates(
    user: User = Depends(get_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [
        prefix(template, template["uuid"])
        for template in data.get_all_templates(user["id"], page, size)
    ]


@router.get("/expand", response_model=List[Template])
async def read_expanded_templates(
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


@router.get("/count", response_model=Count)
async def read_count(user: User = Depends(get_user)):
    return {"count": data.get_user_templates_count(user["id"])}


@router.get("/{uuid}", response_model=TemplateId)
async def read_template_with_id(uuid: UUID):
    template = data.get_template(uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return prefix(template, uuid)


@router.get("/expand/{uuid}", response_model=Template)
async def read_expanded_template_with_id(uuid: UUID):
    template = data.get_template(uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return add_author(prefix(template))


@router.get("/category/{category}", response_model=List[Template])
async def read_templates_by_category(
    category: str,
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [
        add_author(prefix(template))
        for template in data.get_templates_by_category(category, page, size)
    ]


@router.post("/{uuid}", response_model=TemplateId)
async def add_template(uuid: UUID, template: Template, user: User = Depends(get_user)):
    count = data.get_user_templates_count(user["id"])
    template_db = data.get_template(uuid)
    if count < 4 or template_db:
        template.uuid = uuid
        template.author = user["id"]
        data.add_template(template.dict())
    return prefix(template.dict(), uuid)


@router.delete("/{uuid}", response_model=Message)
async def delete_template_with_id(uuid: UUID, user: User = Depends(get_user)):
    data.remove_template(uuid, user["id"])
    if data.get_template(uuid):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "success"}