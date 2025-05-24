from fastapi import FastAPI
from routes.loan_routes import router

app = FastAPI(title="Loan Service", version="1.0.0")

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "This is the Loan Service"}