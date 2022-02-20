import os
import data
import requests

from fastapi import Header, HTTPException, status


def get_user(authorization: str = Header(..., description="e.g. Basic token")):
    user_id = data.get_user_id(authorization)
    if user_id:
        user = data.get_user(user_id)
        user["id"] = user["uid"]
        return user

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
    user["uid"] = user["id"]
    user.pop("id", None)
    data.add_user(user)
    data.add_user_token(authorization, user["id"])
    try:
        user["user_metadata"]["fallback"] = ""
    except:
        user["user_metadata"] = {"fallback": ""}
    data.add_author(
        user["id"],
        user["user_metadata"].get("full_name", ""),
        user["user_metadata"].get("avatar_url", ""),
    )

    user["id"] = user["uid"]
    return user