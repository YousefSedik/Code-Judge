from fastapi import FastAPI, Depends, HTTPException, status
from auth.router import router as auth_router
from problem.router import router as problem_router
from submit.router import router as submit_router
from db import init_db
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()


app.include_router(auth_router, prefix="/auth")
app.include_router(problem_router, prefix="")
app.include_router(submit_router, prefix="")


@app.on_event("startup")
async def on_startup():
    await init_db()
