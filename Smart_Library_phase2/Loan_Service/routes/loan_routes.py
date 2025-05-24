from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schema.loan_schema import LoanCreate, LoanReturn, LoanDetail, LoanHistory,LoanCreateResponse
from service.loanService import LoanService


router = APIRouter(prefix="/api/loans", tags=["Loans"])
loan_service = LoanService()


@router.post("/", response_model=LoanCreateResponse)
async def create_loan(loan_data: LoanCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await loan_service.create_loan(loan_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/returns", response_model=LoanCreateResponse)
async def return_loan(loan_data: LoanReturn, db: AsyncSession = Depends(get_db)):
    try:
        return await loan_service.return_loan(loan_data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{loan_id}", response_model=LoanDetail)
async def get_loan(loan_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await loan_service.get_loan_by_id(loan_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}", response_model=LoanHistory)
async def get_loan_history(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await loan_service.get_loan_history(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
