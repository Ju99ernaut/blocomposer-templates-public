import requests

from fastapi import Header, HTTPException, status
from constants import NETLIFY_USERS_URL


def get_user(authorization: str = Header(...)):
    url = NETLIFY_USERS_URL
    headers = {"authorization": authorization}
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.json()