from typing import Any, Optional
from uuid import UUID, uuid4
from fastapi import Query
from pydantic import BaseModel, Field, AnyHttpUrl

from constants import GJS_PREFIX


class Template(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user: Optional[str] = ""
    name: Optional[str] = ""
    thumbnail: Optional[str] = ""
    preview: Optional[AnyHttpUrl] = ""
    template: Optional[bool] = False
    description: Optional[str] = ""
    assets: Optional[str] = Query("", alias=f"{GJS_PREFIX}assets")
    pages: Optional[str] = Query("", alias=f"{GJS_PREFIX}pages")
    styles: Optional[str] = Query("", alias=f"{GJS_PREFIX}styles")
    views: Optional[int] = 0
    updated_at: Optional[str] = ""


class Asset(BaseModel):
    id: Optional[int] = None
    user: Optional[str] = ""
    name: str
    url: str
    size: int