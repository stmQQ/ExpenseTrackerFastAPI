from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional
from app.models.budget import BudgetPeriod
from app.schemas.category import CategoryRead

from decimal import Decimal
from datetime import date, datetime


class BudgetBase(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    period: BudgetPeriod
    start_date: date
    end_date: Optional[date] = None
    category_id: Optional[int] = None

    @model_validator(mode='after')
    def validate_period(self):
        if self.period == BudgetPeriod.custom and self.end_date is None:
            raise ValueError('end_date is obligatory if period is custom')
        if self.period != BudgetPeriod.custom and self.end_date is not None:
            raise ValueError('end_date can not be specified if period is not custom')
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError('end_date can not be earlier than start_date')
        return self


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    period: Optional[BudgetPeriod] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class BudgetRead(BudgetBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    category: Optional[CategoryRead]

    model_config = ConfigDict(from_attributes=True)


class BudgetWithProgress(BudgetRead):
    spent: Decimal
    remaining: Decimal
    progress_percent: float