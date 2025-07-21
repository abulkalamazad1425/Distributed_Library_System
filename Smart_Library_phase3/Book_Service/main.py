from fastapi import FastAPI
from routes.book_routes import router

app = FastAPI(root_path="/books")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "This is the Book Service"}