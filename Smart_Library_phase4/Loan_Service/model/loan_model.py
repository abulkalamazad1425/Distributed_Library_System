from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta
from database import Base

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, index=True)
    issue_date = Column(DateTime(timezone = True), default=lambda:datetime.now(timezone.utc), nullable=False)
    due_date = Column(DateTime(timezone=True), default = lambda:datetime.now(timezone.utc)+timedelta(days=7), nullable=False)
    return_date = Column(DateTime(timezone.utc), nullable=True)
    status = Column(String, default="ACTIVE", nullable=False)
