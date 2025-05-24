from fastapi import FastAPI
from routes.book_routes import router

app = FastAPI(tittle="Bood Service", version="1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "This is the Book Service"}