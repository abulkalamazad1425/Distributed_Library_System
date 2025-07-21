# create_db.py
from sqlalchemy import create_engine
from model.book_model import Base

# Use sync engine ONLY for table creation
engine = create_engine("postgresql+psycopg2://postgres:user@localhost:5432/book_db")

Base.metadata.create_all(bind=engine)
