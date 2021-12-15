import os
import requests

from fastapi import Header, HTTPException, status


def get_user(authorization: str = Header(..., description="e.g. Basic token")):
    url = os.getenv("NETLIFY_IDENTITY_ENDPOINT") + "/user"
    headers = {"authorization": authorization}
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.json()