from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserOut, UserUpdate
from crud.user import UserService 
from database import AsyncSessionLocal

router = APIRouter(prefix="/api/users", tags=["Users"])
user_crud = UserService()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_crud.create_user(db, user.dict())
    return new_user

@router.get("/{user_id}", response_model=UserOut)
async def fetch_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated = await user_crud.update_user(db, user_id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
