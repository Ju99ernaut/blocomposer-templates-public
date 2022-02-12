import data

from fastapi import APIRouter, Query
from models import Email, Message

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/subscribe", response_model=Message)
async def subscribe_to_newsletter(email: Email):
    data.add_email(email.dict())
    return {"msg": "success"}


@router.get("/subscribe", response_model=Message)
async def subscribe_to_newsletter_using_querystring(
    email: str = Query(..., description="Email to register")
):
    data.add_email(Email(email=email).dict())
    return {"msg": "success"}


@router.post("/unsubscribe", response_model=Message)
async def unsubscribe_to_newsletter(email: Email):
    data.remove_email(email.email)
    return {"msg": "success"}


@router.get("/unsubscribe", response_model=Message)
async def unsubscribe_to_newsletter_using_querystring(
    email: str = Query(..., description="Email to register")
):
    data.remove_email(email)
    return {"msg": "success"}