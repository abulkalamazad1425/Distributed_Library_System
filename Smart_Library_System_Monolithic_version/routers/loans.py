from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.loan import *
from crud.loan import LoanService
from database import get_db

router = APIRouter(prefix="/api", tags=["Loans"])
loan_service = LoanService()

@router.post("/loans", response_model=LoanOut)
async def issue_book(loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    return await loan_service.issue_book(db, loan)

@router.post("/returns", response_model=LoanOut)
async def return_book(req: ReturnRequest, db: AsyncSession = Depends(get_db)):
    result = await loan_service.return_book(db, req.loan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Loan not found")
    return result

@router.get("/loans/overdue", response_model=List[LoanOut])
async def get_overdue(db: AsyncSession = Depends(get_db)):
    return await loan_service.get_overdue_loans(db)

@router.put("/loans/{loan_id}/extend", response_model=LoanExtendOut)
async def extend_loan(loan_id: int, req: ExtendRequest, db: AsyncSession = Depends(get_db)):
    loan = await loan_service.extend_loan(db, loan_id, req.extension_days)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.get("/loans/{user_id}", response_model=List[LoanOut])
async def user_loans(user_id: int, db: AsyncSession = Depends(get_db)):
    return await loan_service.get_loans_by_user(db, user_id)
