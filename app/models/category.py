from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import enum


class CategoryType(str, enum.Enum):
    income = 'income'
    expense = 'expense'


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[CategoryType] = mapped_column(Enum(CategoryType))
    color = Mapped[str | None] = mapped_column(String(7), nullable=True)

    user = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category')
    budgets = relationship('Budget', back_populates='category')