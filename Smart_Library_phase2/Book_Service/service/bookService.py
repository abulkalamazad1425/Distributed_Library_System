from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.book_model import Book
from schema.book_schema import BookCreate, BookUpdate
from aiobreaker import CircuitBreaker
import asyncio

breaker = CircuitBreaker(
    fail_max=5,        
    timeout_duration=30   
)

TIMEOUT_SECONDS = 5

class BookService:

    @breaker
    async def create_book(self, book: BookCreate, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._create_book(book, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while creating book")

    async def _create_book(self, book: BookCreate, db: AsyncSession):
        now = datetime.now(timezone.utc)
        new_book = Book(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            copies=book.copies,
            available_copies=book.copies,
            created_at=now,
            updated_at=now
        )
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book

    @breaker
    async def get_books_by_search(self, search: str, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._get_books_by_search(search, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while searching books")

    async def _get_books_by_search(self, search: str, db: AsyncSession):
        query = select(Book).where(
            Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%")
        )
        result = await db.execute(query)
        return result.scalars().all()

    @breaker
    async def get_book_by_id(self, book_id: int, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._get_book_by_id(book_id, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while retrieving book by ID")

    async def _get_book_by_id(self, book_id: int, db: AsyncSession):
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    @breaker
    async def update_book(self, book_id: int, book: BookUpdate, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._update_book(book_id, book, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while updating book")

    async def _update_book(self, book_id: int, book: BookUpdate, db: AsyncSession):
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalar_one_or_none()
        if not db_book:
            return None

        copy_add = (book.copies - db_book.copies) if book.copies else 0

        if book.copies:
            db_book.copies = book.copies

        if book.available_copies is not None:
            db_book.available_copies = book.available_copies
        else:
            db_book.available_copies += copy_add

        db_book.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_book)
        return db_book

    @breaker
    async def update_book_availability(self, book_id: int, book: BookUpdate, db: AsyncSession):
        try:
            return await asyncio.wait_for(self._update_book_availability(book_id, book, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while updating availability")

    async def _update_book_availability(self, book_id: int, book: BookUpdate, db: AsyncSession):
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalar_one_or_none()
        if not db_book:
            return None

        if book.operation == "increment":
            db_book.available_copies += book.available_copies
        elif book.operation == "decrement":
            if db_book.available_copies < book.available_copies:
                raise ValueError("Not enough available copies to decrement")
            db_book.available_copies -= book.available_copies
        else:
            raise ValueError("Invalid operation type: must be 'increment' or 'decrement'")

        db_book.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_book)
        return db_book

    @breaker
    async def delete_book(self, book_id: int, db: AsyncSession) -> bool:
        try:
            return await asyncio.wait_for(self._delete_book(book_id, db), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout while deleting book")

    async def _delete_book(self, book_id: int, db: AsyncSession) -> bool:
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return False
        await db.delete(book)
        await db.commit()
        return True
