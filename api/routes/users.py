from uuid import UUID
from fastapi import APIRouter, Depends
from models import User
from dependencies import get_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=User)
async def read_user(
    user: User = Depends(get_user),
):
    return user
