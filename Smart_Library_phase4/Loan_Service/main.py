# loan-service/main.py
from fastapi import FastAPI
from model.loan_model import Loan  # Import your loan model

from routes.loan_routes import router
from database import engine, Base
import asyncio

app = FastAPI(root_path="/loans")

app.include_router(router)

@app.on_event("startup")
async def on_startup():
    # Create tables in the database if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "This is the Loan Service"}
