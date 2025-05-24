from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update, delete, or_
from models.book import Book
from datetime import datetime, timezone
from typing import List, Optional


class BookService:

    async def create_book(self, db: AsyncSession, book_data: dict) -> Book:
        now = datetime.now(timezone.utc)

        book_data["available_copies"] = book_data["copies"]
        book_data["created_at"] = now
        book_data["updated_at"] = now

        new_book = Book(**book_data)
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    async def get_book(self, db: AsyncSession, book_id: int) -> Optional[Book]:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    async def update_book(self, db: AsyncSession, book_id: int, updates: dict) -> Optional[Book]:
        updates["updated_at"] = datetime.now(timezone.utc)

        await db.execute(update(Book).where(Book.id == book_id).values(**updates))
        await db.commit()
        return await self.get_book(db, book_id)

    async def delete_book(self, db: AsyncSession, book_id: int):
        await db.execute(delete(Book).where(Book.id == book_id))
        await db.commit()

    async def search_books(self, db: AsyncSession, query: str) -> List[Book]:
        result = await db.execute(
            select(Book).where(
                or_(
                    Book.title.ilike(f"%{query}%"),
                    Book.author.ilike(f"%{query}%"),
                    Book.isbn.ilike(f"%{query}%")
                )
            )
        )
        return result.scalars().all()
    
   
   

    async def decrement_copy(self, db: AsyncSession, book_id: int):
        await db.execute(
            update(Book)
            .where(Book.id == book_id, Book.available_copies > 0)
            .values(available_copies=Book.available_copies - 1)
        )
        await db.commit()

    async def increment_copy(self, db: AsyncSession, book_id: int):
        await db.execute(
            update(Book).where(Book.id == book_id)
            .values(available_copies=Book.available_copies + 1)
        )
        await db.commit()


    

    async def count_books(self, db: AsyncSession) -> int:
        result = await db.execute(select(Book))
        return len(result.scalars().all())


    async def count_available_books(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.sum(Book.available_copies)))
        return result.scalar() or 0

    async def get_book_summary(self, db: AsyncSession, book_id: int):
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar()