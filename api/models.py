from typing import List, Optional, Union
from uuid import UUID, uuid4
from fastapi import Query
from pydantic import BaseModel, Field, AnyHttpUrl, validator
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
    author: Union[Author, str]
    name: Optional[str] = ""
    category: Optional[str] = "default"
    thumbnail: Optional[str] = ""
    preview: Optional[AnyHttpUrl] = ""
    template: Optional[bool] = False
    public: Optional[bool] = False
    description: Optional[str] = ""
    assets: Optional[str] = Query("", alias=f"{GJS_PREFIX}assets")
    pages: Optional[str] = Query("", alias=f"{GJS_PREFIX}pages")
    styles: Optional[str] = Query("", alias=f"{GJS_PREFIX}styles")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class Asset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Union[Author, str]
    name: str
    url: str
    size: Optional[int] = 0
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class Bookmark(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    author: str
    bookmarks: Union[List[str], str]
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    @validator("bookmarks")
    def stringify(cls, v):
        if type(v) == list:
            return ",".join(v)
        return v


class BookmarkRef(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Author
    bookmarks: Union[List[str], str]
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    @validator("bookmarks")
    def listify(cls, v):
        if type(v) == str:
            return v.split(",")
        return v


class Comment(BaseModel):
    comment: str


class CommentRef(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    author: Union[Author, str]
    template: UUID = Field(default_factory=uuid4)
    comment: str
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class Block(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    category: str
    description: Optional[str] = "Custom block"
    html: str
    css: Optional[str] = ""
    thumbnail: Optional[str] = ""
    author: Union[Author, str]
    template: UUID = Field(default_factory=uuid4)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class Message(BaseModel):
    msg: Optional[str] = "success"


class Count(BaseModel):
    count: Optional[int] = 0