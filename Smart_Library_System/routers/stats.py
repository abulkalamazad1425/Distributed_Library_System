from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud.stat import StatisticsService

router = APIRouter(prefix="/api/stats", tags=["Statistics"])
stats_service = StatisticsService()

@router.get("/books/popular")
async def get_popular_books(db: AsyncSession = Depends(get_db)):
    return await stats_service.get_most_borrowed_books(db)

@router.get("/users/active")
async def get_active_users(db: AsyncSession = Depends(get_db)):
    return await stats_service.get_most_active_users(db)

@router.get("/overview")
async def get_system_overview(db: AsyncSession = Depends(get_db)):
    return await stats_service.get_system_overview(db)