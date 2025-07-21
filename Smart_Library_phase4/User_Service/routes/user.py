from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from service.userService import userService
from schema.user_schema import UserOut, UserCreate, CreateResponse, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])
userService = userService()

@router.post("/", response_model=CreateResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await userService.create_user(user, db)
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))

@router.get("/{u_id}", response_model=UserOut)
async def get_users(u_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await userService.get_user(u_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))

@router.put("/{u_id}", response_model=UserOut)
async def update_user(u_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_user = await userService.update_user(u_id, user, db)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
