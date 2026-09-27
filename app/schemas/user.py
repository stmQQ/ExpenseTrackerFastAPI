from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional

from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserRead):
    hashed_password: str