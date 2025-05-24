from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime



class LoanReturn(BaseModel):
    loan_id: int


class LoanCreateResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

class BookInfo(BaseModel):
    id: int
    title: str
    author: str


class UserInfo(BaseModel):
    id: int
    name: str
    email: str


class LoanDetail(BaseModel):
    id: int
    user: UserInfo
    book: BookInfo
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str


class LoanSummary(BaseModel):
    id: int
    book: BookInfo
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str


class LoanHistory(BaseModel):
    loans: List[LoanSummary]
    total: int
