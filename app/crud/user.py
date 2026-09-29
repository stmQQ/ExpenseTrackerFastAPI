from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserLogin


async def get_by_id(
        db: AsyncSession, 
        user_id: int
) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_email(
        db: AsyncSession, 
        user_email: str
) -> User | None:
    result = await db.execute(select(User).where(User.email == user_email))
    return result.scalar_one_or_none()


async def create(
        db: AsyncSession, 
        obj_in: UserCreate
) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        is_active=True
    )
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def update(
        db: AsyncSession, 
        db_obj: User, 
        obj_in: UserUpdate
) -> User:
    update_data = obj_in.model_dump(exclude_unset=True)

    if 'password' in update_data:
        hashed = get_password_hash(update_data.pop('password'))
        update_data['hashed_password'] = hashed

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def authenticate(
        db: AsyncSession, 
        obj_in: UserLogin
) -> User | None:
    user = await get_by_email(db, email=obj_in.email)
    if user is None:
        return None
    if not verify_password(obj_in.password, user.hashed_password):
        return None
    return user


async def is_active(user: User) -> bool:
    return user.is_active