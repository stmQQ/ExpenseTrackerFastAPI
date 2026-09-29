from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get_by_id(
        db: AsyncSession,
        category_id: int,
        user_id: int
) -> Category | None:
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id)
    )

    return result.scalar_one_or_none()


async def get_multi(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
) -> list[Category]:
    result = await db.execute(
        select(Category).where(
            Category.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Category.id)
    )

    return list(result.scalars().all())


async def create(
        db: AsyncSession,
        obj_in: CategoryCreate,
        user_id: int
) -> Category:
    db_obj = Category(
        **obj_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def update(
        db: AsyncSession,
        db_obj: Category,
        obj_in: CategoryUpdate
) -> Category:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.flush()
    db.execute(db_obj)
    return db_obj


async def delete(
        db: AsyncSession,
        db_obj: Category
) -> None:
    await db.delete(db_obj)
    await db.flush()
