from fastapi import FastAPI

from routes.user import router


app = FastAPI(root_path="/users")

app.router.include_router(router, prefix="/api", tags=["user"])


@app.get("/")
async def root():
    return {"message": "Hello World"}