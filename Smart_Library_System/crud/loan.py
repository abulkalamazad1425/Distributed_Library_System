from datetime import datetime, timedelta, timezone
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.book import BookService
from models.loan import Loan
from schemas.loan import LoanCreate

class LoanService:
    def __init__(self):
        self.book_service = BookService()


    async def issue_book(self, db: AsyncSession, loan_data: LoanCreate) -> Loan:
        now_utc = datetime.now(timezone.utc)
        due_utc = now_utc + timedelta(days=7)

        new_loan = Loan(
            user_id=loan_data.user_id,
            book_id=loan_data.book_id,
            issue_date=now_utc,
            due_date=due_utc,
            return_date=None,
            status="ACTIVE",
            extensions_count=0
        )
        db.add(new_loan)
        await self.book_service.decrement_copy(db, loan_data.book_id)
        await db.commit()
        await db.refresh(new_loan)
        return new_loan

    async def return_book(self, db: AsyncSession, loan_id: int) -> Loan:
        loan = await db.get(Loan, loan_id)
        if not loan:
            return None

        loan.return_date = datetime.now(timezone.utc)
        loan.status = "RETURNED"

        await self.book_service.increment_copy(db, loan.book_id)
        await db.commit()
        await db.refresh(loan)
        return loan

    async def get_overdue_loans(self, db: AsyncSession):
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(Loan).where(Loan.due_date < now, Loan.status == "ACTIVE")
        )
        return result.scalars().all()
    
    async def extend_loan(self, db: AsyncSession, loan_id: int, extension_days: int) -> Loan:
        loan = await db.get(Loan, loan_id)
        if not loan:
            return None

        loan.due_date += timedelta(days=extension_days)
        loan.extensions_count += 1

        await db.commit()
        await db.refresh(loan)
        return loan
    
    #methods for statistics

    async def get_loans_by_user(self, db: AsyncSession, user_id: int):
        return (
            await db.execute(select(Loan).where(Loan.user_id == user_id))
        ).scalars().all()
    
    async def count_active_loans(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).where(Loan.status == 'ACTIVE'))
        return result.scalar()

    async def count_active_loans_by_user(self, db: AsyncSession, user_id: int) -> int:
        result = await db.execute(select(func.count()).where(Loan.user_id == user_id, Loan.status == 'ACTIVE'))
        return result.scalar()

    async def count_overdue_loans(self, db: AsyncSession) -> int:
        from datetime import datetime
        now = datetime.utcnow()
        result = await db.execute(
            select(func.count()).where(Loan.due_date < now, Loan.status == 'ACTIVE')
        )
        return result.scalar()

    async def count_loans_since(self, db: AsyncSession, since: datetime) -> int:
        result = await db.execute(select(func.count()).where(Loan.issue_date >= since))
        return result.scalar()

    async def count_returns_since(self, db: AsyncSession, since: datetime) -> int:
        result = await db.execute(select(func.count()).where(Loan.return_date >= since))
        return result.scalar()

    async def get_borrow_counts_by_book(self, db: AsyncSession):
        result = await db.execute(
            select(Loan.book_id, func.count().label("borrow_count"))
            .group_by(Loan.book_id)
            .order_by(desc("borrow_count"))
            .limit(5)
        )
        return result.all()

    async def get_borrow_counts_by_user(self, db: AsyncSession):
        result = await db.execute(
            select(Loan.user_id, func.count().label("books_borrowed"))
            .group_by(Loan.user_id)
            .order_by(desc("books_borrowed"))
            .limit(5)
        )
        return result.all()
