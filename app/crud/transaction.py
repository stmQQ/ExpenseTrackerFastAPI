from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import date
from decimal import Decimal

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


async def get_by_id(
        db: AsyncSession, 
        transaction_id: int, 
        user_id: int
) -> Transaction | None:
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id, 
            Transaction.user_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def get_multi(
        db: AsyncSession,
        user_id: int,
        skip: int = 0, 
        limit: int = 100, 
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None
) -> list[Transaction]:
    query = (
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.user_id == user_id)
    )

    if category_id is not None:
        query = query.where(Transaction.category_id == category_id)
    if date_from is not None:
        query = query.where(Transaction.date >= date_from)
    if date_to is not None:
        query = query.where(Transaction.date <= date_to)

    query = query.order_by(Transaction.date.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def create(
        db: AsyncSession,
        obj_in: TransactionCreate,
        user_id: int
) -> Transaction:
    db_obj = Transaction(
        **obj_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.flush()
    db.refresh(db_obj)
    return db_obj


async def update(
        db: AsyncSession,
        db_obj: Transaction,
        obj_in: TransactionUpdate
) -> Transaction:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.flush()
    db.refresh(db_obj)
    return db_obj


async def delete(
        db: AsyncSession,
        db_obj: Transaction
) -> None:
    await db.delete(db_obj)
    await db.flush()


async def get_sum(
        db: AsyncSession,
        user_id: int,
        date_from: date | None = None,
        date_to: date | None = None,
        category_id: int | None = None
) -> Decimal:
    query = select(
        func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id)

    if category_id is not None:
        query = query.where(Transaction.category_id == category_id)
    if date_from is not None:
        query = query.where(Transaction.date >= date_from)
    if date_to is not None:
        query = query.where(Transaction.date <= date_to)

    result = await db.execute(query)
    return result.scalar_one()