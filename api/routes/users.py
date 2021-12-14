from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from models import User

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=User)
async def read_user():
    return {"id": "jdjbfiruhgjdnbv"}
