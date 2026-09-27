from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.schemas.category import CategoryRead

from decimal import Decimal
from datetime import date, datetime


class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    description: Optional[str] = Field(None, max_length=500)
    date: date
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=2)
    description: Optional[str] = Field(None, max_length=500)
    date: Optional[date] = None
    category_id: Optional[int] = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    category: CategoryRead

    model_config = ConfigDict(from_attributes=True)