from sqlalchemy import Integer, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User

 
class UserService:
    async def create_user(self, db: AsyncSession, user_data: dict):        
        new_user = User(**user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def get_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


    async def update_user(self, db: AsyncSession, user_id: int, updates: dict):
        user_service = UserService()
        user = await user_service.get_user(db, user_id)
        if not user:
            return None
        for key, value in updates.items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user    
    
    
    async def count_users(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(User))
        return result.scalar()

    async def get_user_summary(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar()

