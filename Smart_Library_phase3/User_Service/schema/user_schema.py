from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserCreate(BaseModel):    
    name: str
    email: EmailStr
    role: str

class CreateResponse(UserCreate):
    id:int
    created_at: datetime
    def config(self):
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
   
class UserOut(CreateResponse):
    updated_at: datetime
    def config(self):
        orm_mode = True


