from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.user_model import User
from schema.user_schema import UserCreate, UserUpdate
from datetime import datetime, timezone
import asyncio
from aiobreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, timeout_duration=30)


class userService:
    @breaker
    async def create_user(self, user: UserCreate, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._create_user(user, db), timeout=3.0)
        except asyncio.TimeoutError:
            raise TimeoutError("User creation timed out")

    async def _create_user(self, user: UserCreate, db: AsyncSession):
        new_user = User(
            name=user.name,
            email=user.email,
            role=user.role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @breaker
    async def get_user(self, u_id: int, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._get_user(u_id, db), timeout=3.0)
        except asyncio.TimeoutError:
            raise TimeoutError("User fetch timed out")

    async def _get_user(self, u_id: int, db: AsyncSession):
        result = await db.execute(select(User).where(User.id == u_id))
        return result.scalar_one_or_none()

    @breaker
    async def update_user(self, u_id: int, user: UserUpdate, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._update_user(u_id, user, db), timeout=3.0)
        except asyncio.TimeoutError:
            raise TimeoutError("User update timed out")

    async def _update_user(self, u_id: int, user: UserUpdate, db: AsyncSession):
        result = await db.execute(select(User).where(User.id == u_id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
        if user.role:
            db_user.role = user.role
        db_user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_user)
        return db_user
