from pydantic import Basemodel, ConfigDict, Field
from typing import Optional
from app.models.category import CategoryType


class CategoryBase(Basemodel):
    name: str = Field(..., min_length=1, max_length=100)
    type: CategoryType
    color: Optional[str] = Field(None, pattern='^#[0-9A-Fa-f]{6}$')


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[CategoryType] = None
    color: Optional[str] = Field(None, pattern='^#[0-9A-Fa-f]{6}$')


class CategoryRead(CategoryBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)