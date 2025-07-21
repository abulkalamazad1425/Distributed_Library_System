from pydantic import BaseModel       
from typing import Optional, List,Literal
from datetime import datetime

class BookBase(BaseModel):
    title:str
    author:str
    isbn:str
    copies:int

class BookCreate(BookBase):
    pass 

class BookUpdate(BaseModel):
    copies: Optional[int] = None
    available_copies: Optional[int] = None

class BookOut(BookCreate):
    
    available_copies: int
    id:int
    created_at: datetime
    updated_at: datetime
    def config(self):
        orm_mode = True

class BookListResponse(BaseModel):
    books: List[BookOut]
    total: int
    def config(self):
        orm_mode = True



class BookAvailabilityUpdate(BaseModel):
    available_copies: int
    operation: Literal["increment","decrement"]

class BookAvailabilityResponse(BaseModel):
    id:int
    available_copies: int
    updated_at: datetime
    def config(self):
        orm_mode = True