from fastapi import FastAPI
from routes.loan_routes import router

app = FastAPI(root_path="/loans")

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "This is the Loan Service"}