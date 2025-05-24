from fastapi import FastAPI

from routes.user import router


app = FastAPI()

app.router.include_router(router, prefix="/api/user", tags=["user"])


@app.get("/")
async def root():
    return {"message": "Hello World"}