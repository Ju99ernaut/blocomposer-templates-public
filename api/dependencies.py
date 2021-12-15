import os
import data
import requests

from fastapi import Header, HTTPException, status


def get_user(authorization: str = Header(..., description="e.g. Basic token")):
    user_id = data.get_user_id(authorization)
    if user_id:
        return data.get_user(user_id)

    url = os.getenv("NETLIFY_IDENTITY_ENDPOINT") + "/user"
    headers = {"authorization": authorization}
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = result.json()
    data.add_user(user)
    data.add_user_token(authorization, user["id"])

    return user