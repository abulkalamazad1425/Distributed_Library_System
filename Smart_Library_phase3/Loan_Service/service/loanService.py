from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.loan_model import Loan
from schema.loan_schema import LoanCreate, LoanReturn
import httpx
from httpx import TimeoutException, RequestError

USER_SERVICE_URL = "http://user-service:8081/api/user"
BOOK_SERVICE_URL = "http://book-service:8082/api/book"
TIMEOUT_SECONDS = 5


class LoanService:
    async def create_loan(self, loan_data: LoanCreate, db: AsyncSession):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                user_resp = await client.get(f"{USER_SERVICE_URL}/{loan_data.user_id}")
                user_resp.raise_for_status()
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to validate user: " + str(e))

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                book_resp = await client.get(f"{BOOK_SERVICE_URL}/{loan_data.book_id}")
                book_resp.raise_for_status()
                book_data = book_resp.json()
                if book_data["available_copies"] < 1:
                    raise ValueError("Book not available")
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to validate book availability: " + str(e))

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                patch_resp = await client.patch(
                    f"{BOOK_SERVICE_URL}/{loan_data.book_id}/availability",
                    json={"operation": "decrement", "available_copies": 1}
                )
                patch_resp.raise_for_status()
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to decrement book availability: " + str(e))

        loan = Loan(
            user_id=loan_data.user_id,
            book_id=loan_data.book_id,
            issue_date=datetime.now(timezone.utc),
            due_date=loan_data.due_date,
            status="ACTIVE"
        )
        db.add(loan)
        await db.commit()
        await db.refresh(loan)
        #loan.remove("return_date")  # Exclude return_date from the response
        return loan

    async def return_loan(self, return_data: LoanReturn, db: AsyncSession):
        result = await db.execute(select(Loan).where(Loan.id == return_data.loan_id))
        loan = result.scalar_one_or_none()
        if not loan:
            raise ValueError("Loan not found")
        if loan.status == "RETURNED":
            raise ValueError("Loan already returned")
        

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                patch_resp = await client.patch(
                    f"{BOOK_SERVICE_URL}/{loan.book_id}/availability",
                    json={"operation": "increment", "available_copies": 1}
                )
                patch_resp.raise_for_status()
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to increment book availability: " + str(e))

        loan.return_date = datetime.now(timezone.utc)
        loan.status = "RETURNED"
        await db.commit()
        await db.refresh(loan)
        return loan

    async def get_loan_by_id(self, loan_id: int, db: AsyncSession):
        result = await db.execute(select(Loan).where(Loan.id == loan_id))
        loan = result.scalar_one_or_none()
        if not loan:
            raise ValueError("Loan not found")
        

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                user_resp = await client.get(f"{USER_SERVICE_URL}/{loan.user_id}")
                user_resp.raise_for_status()
                user = user_resp.json()
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to fetch user details: " + str(e))

        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                book_resp = await client.get(f"{BOOK_SERVICE_URL}/{loan.book_id}")
                book_resp.raise_for_status()
                book = book_resp.json()
        except (TimeoutException, RequestError) as e:
            raise ConnectionError("Failed to fetch book details: " + str(e))

        return {
            "id": loan.id,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            },
            "book": {
                "id": book["id"],
                "title": book["title"],
                "author": book["author"]
            },
            "issue_date": loan.issue_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "status": loan.status
        }

    async def get_loan_history(self, user_id: int, db: AsyncSession):
        result = await db.execute(select(Loan).where(Loan.user_id == user_id))
        loans = result.scalars().all()

        loan_list = []
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            for loan in loans:
                try:
                    book_resp = await client.get(f"{BOOK_SERVICE_URL}/{loan.book_id}")
                    book_resp.raise_for_status()
                    book = book_resp.json()
                except (TimeoutException, RequestError) as e:
                    raise ConnectionError("Failed to fetch book details for loan: " + str(e))

                loan_list.append({
                    "id": loan.id,
                    "book": {
                        "id": book["id"],
                        "title": book["title"],
                        "author": book["author"]
                    },
                    "issue_date": loan.issue_date,
                    "due_date": loan.due_date,
                    "return_date": loan.return_date,
                    "status": loan.status
                })

        return {
            "loans": loan_list,
            "total": len(loan_list)
        }
