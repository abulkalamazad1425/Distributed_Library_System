# user-service/main.py
from fastapi import FastAPI
from routes.user import router  # your user router
from database import engine, Base  # from database.py
from model.user_model import User  # your user model

app = FastAPI(root_path="/users")

# Include the router under /users/api/
app.include_router(router, prefix="/api", tags=["user"])

# Auto-create tables at startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Test root
@app.get("/")
async def root():
    return {"message": "Hello World"}
