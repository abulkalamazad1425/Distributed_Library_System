# models/loan.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    issue_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    due_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="ACTIVE")
    extensions_count = Column(Integer, default=0)
