from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import date

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


async def get_by_id(
        db: AsyncSession,
        budget_id: int,
        user_id: int
) -> Budget | None:
    result = await db.execute(
        select(Budget)
        .options(selectinload(Budget.category))
        .where(
            Budget.id == budget_id,
            Budget.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def get_multi(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = False
) -> list[Budget]:
    query = (
        select(Budget)
        .options(selectinload(Budget.category))
        .where(Budget.user_id == user_id)
    )

    if only_active:
        query = query.where(Budget.is_active.is_(True))

    query = query.order_by(Budget.start_date.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def create(
        db: AsyncSession,
        obj_in: BudgetCreate,
        user_id: int
) -> Budget:
    db_obj = Budget(
        **obj_in.model_dump(),
        user_id=user_id
    )

    db.add(db_obj)
    db.flush()
    db.refresh(db_obj)
    return db_obj


async def update(
    db: AsyncSession,
    db_obj: Budget,
    obj_in: BudgetUpdate,
) -> Budget:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def delete(
    db: AsyncSession,
    db_obj: Budget,
) -> None:
    await db.delete(db_obj)
    await db.flush()