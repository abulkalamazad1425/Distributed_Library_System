# book-service/main.py
from fastapi import FastAPI
from model.book_model import Book
from routes.book_routes import router
from database import engine, Base
  # Import your book model
app = FastAPI(root_path="/books")

app.include_router(router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "This is the Book Service"}
