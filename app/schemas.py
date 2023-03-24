from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, SecretStr, conint, validator

import re


from .validate_funtions import validate_email


class UserBase(BaseModel):
    email: str
    password: str
    


class User(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: UUID
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None


class Vote(BaseModel):
    post_id: str
    like: bool
    comment: Optional[str] = None
    dir: conint(le=1)
