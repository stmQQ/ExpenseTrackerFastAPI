from sqlalchemy import ForeignKey, Date, DateTime, Text, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from datetime import date, datetime
from decimal import Decimal


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='RESTRICT'))

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[date] = mapped_column(Date())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')