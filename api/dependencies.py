import requests
import json

from fastapi import Header, HTTPException

from constants import NETLIFY_USERS_URL


def get_user(authorization):
    url = NETLIFY_USERS_URL
    headers = {"authorization": authorization}
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        return None
    return result.json()