from typing import Optional, Union
from uuid import UUID, uuid4
from fastapi import Query
from pydantic import BaseModel, Field, AnyHttpUrl
from datetime import datetime

from constants import GJS_PREFIX


class User(BaseModel):
    id: str
    role: str
    aud: str
    url: str
    confirmed_at: Union[datetime, str]
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    invited_at: Union[datetime, str]


class Author(BaseModel):
    id: str
    avatar_url: str
    full_name: str


class Template(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Optional[Union[Author, str]] = None
    name: Optional[str] = ""
    category: Optional[str] = "default"
    thumbnail: Optional[str] = ""
    preview: Optional[str] = ""
    template: Optional[bool] = False
    public: Optional[bool] = False
    description: Optional[str] = ""
    assets: Optional[str] = Query("", alias=f"{GJS_PREFIX}assets")
    pages: Optional[str] = Query("", alias=f"{GJS_PREFIX}pages")
    styles: Optional[str] = Query("", alias=f"{GJS_PREFIX}styles")
    framework: Optional[str] = "none"
    updated_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Asset(BaseModel):
    id: str
    author: Optional[Union[Author, str]] = None
    name: str
    caption: str
    src: str
    size: Optional[int] = 0
    updated_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Bookmark(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Optional[Union[Author, str]] = None
    template: Union[Template, UUID]
    updated_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Comment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Optional[Union[Author, str]] = None
    template: UUID = Field(default_factory=uuid4)
    comment: str
    updated_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Block(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: Optional[str] = None
    category: Optional[str] = "default"
    description: Optional[str] = "Custom block"
    html: Optional[str] = ""
    css: Optional[str] = ""
    thumbnail: Optional[str] = ""
    author: Optional[Union[Author, str]] = None
    template: UUID = Field(default_factory=uuid4)
    updated_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Email(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    subscribed_at: Optional[Union[datetime, str]] = Field(default_factory=datetime.now)


class Message(BaseModel):
    msg: Optional[str] = "success"


class Count(BaseModel):
    count: Optional[int] = 0