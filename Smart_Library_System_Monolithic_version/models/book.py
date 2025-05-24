from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False) 
    created_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
