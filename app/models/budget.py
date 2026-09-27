from sqlalchemy import String, DateTime, Date, Numeric, ForeignKey, Enum, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from decimal import Decimal
from datetime import date, datetime
import enum


class BudgetPeriod(str, enum.Enum):
    month = 'month'
    year = 'year'
    custom = 'custom'


class Budget(Base):
    __tablename__ = 'budgets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    period: Mapped[BudgetPeriod] = mapped_column(Enum(BudgetPeriod))
    start_date: Mapped[date] = mapped_column(Date)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='budgets')
    category = relationship('Category', back_populates='budgets')