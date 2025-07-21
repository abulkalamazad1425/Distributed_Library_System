from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    copies = Column(Integer)
    available_copies = Column(Integer)
    created_at = Column(DateTime(timezone.utc), default=lambda:datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone.utc), default=lambda:datetime.now(timezone.utc), nullable=False)

    