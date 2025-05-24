from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import BookCreate, BookUpdate, BookOut
from crud.book import BookService
from database import get_db
from typing import List

router = APIRouter(prefix="/api/books", tags=["Books"])
book_service = BookService()

@router.post("/", response_model=BookOut)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await book_service.create_book(db, book.dict())

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: int, updates: BookUpdate, db: AsyncSession = Depends(get_db)):
    book = await book_service.update_book(db, book_id, updates.dict(exclude_unset=True))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    await book_service.delete_book(db, book_id)
    return {"message": "Book deleted"}

@router.get("/", response_model=List[BookOut])
async def search_books(search: str, db: AsyncSession = Depends(get_db)):
    return await book_service.search_books(db, search)
