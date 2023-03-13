from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, SecretStr, validator

import re
from .validate_funtions import validate_email


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
