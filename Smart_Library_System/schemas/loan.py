from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional

class LoanCreate(BaseModel):
    user_id: int
    book_id: int
   
class ReturnRequest(BaseModel):
    loan_id: int

class ExtendRequest(BaseModel):
    extension_days: int

class LoanOut(BaseModel):
    id: int
    user_id: Optional[int]
    book_id: Optional[int]
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

class LoanExtendOut(LoanOut):
    extensions_count: int

class BookInfo(BaseModel):
    id: int
    title: str
    author: str

class LoanWithBookOut(BaseModel):
    id: int
    book: BookInfo
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str
