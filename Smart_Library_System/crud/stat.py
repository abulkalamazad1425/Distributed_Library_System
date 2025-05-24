from sqlalchemy.ext.asyncio import AsyncSession
from crud.book import BookService
from crud.user import UserService
from crud.loan import LoanService
from datetime import datetime

class StatisticsService:
    def __init__(self):
        self.book_service = BookService()
        self.user_service = UserService()
        self.loan_service = LoanService()

    async def get_most_borrowed_books(self, db: AsyncSession):
        borrow_counts = await self.loan_service.get_borrow_counts_by_book(db)
        books = []
        for record in borrow_counts:
            book = await self.book_service.get_book_summary(db, record.book_id)
            if book:
                books.append({
                    "book_id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "borrow_count": record.borrow_count
                })
        return books

    async def get_most_active_users(self, db: AsyncSession):
        borrow_counts = await self.loan_service.get_borrow_counts_by_user(db)
        users = []
        for record in borrow_counts:
            user = await self.user_service.get_user_summary(db, record.user_id)
            if user:
                current_borrows = await self.loan_service.count_active_loans_by_user(db, record.user_id)
                users.append({
                    "user_id": user.id,
                    "name": user.name,
                    "books_borrowed": record.books_borrowed,
                    "current_borrows": current_borrows
                })
        return users

    async def get_system_overview(self, db: AsyncSession):
        available_books = await self.book_service.count_available_books(db)
        borrowed_books = await self.loan_service.count_active_loans(db)
        total_books = available_books + borrowed_books
        total_users = await self.user_service.count_users(db)
        overdue_loans = await self.loan_service.count_overdue_loans(db)

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        loans_today = await self.loan_service.count_loans_since(db, today_start)
        returns_today = await self.loan_service.count_returns_since(db, today_start)

        return {
            "total_books": total_books,
            "total_users": total_users,
            "books_available": available_books,
            "books_borrowed": borrowed_books,
            "overdue_loans": overdue_loans,
            "loans_today": loans_today,
            "returns_today": returns_today
        }
