from fastapi import FastAPI
from routers import users, books, loans,stats

app = FastAPI(title="Smart Library System", version="1.0.0")

app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(stats.router)
 

@app.get("/")
async def about():
    msg = {
        "message": "Welcome to the Smart Library System API",
    }
    return msg 