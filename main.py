from fastapi import FastAPI
from auth.router import router as auth_router
from problem.router import router as problem_router
from submit.router import router as submit_router
from db import init_db
import uvicorn

# from contextlib import asynccontextmanager


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await init_db()
#     yield


app = FastAPI()


app.include_router(
    auth_router, prefix="/auth", tags=["user authentication and registration"]
)
app.include_router(problem_router, prefix="", tags=["add or get problems"])
app.include_router(submit_router, prefix="", tags=["submit or get a solution"])


if __name__ == "__main__":

    uvicorn.run(app)
