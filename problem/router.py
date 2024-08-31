from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from sqlmodel import select
from problem.models import Problem

router = APIRouter()


@router.get("/problem/<problem_id>")
async def get_problem(problem_id: int, session: AsyncSession = Depends(get_session)):
    problem_info = await session.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem_info = problem_info.scalars().first()
    print(problem_info)
    if problem_info is None:
        raise HTTPException("Problem not found", status_code=404)
    return problem_info.to_dict()


@router.post("/problem/manual")
async def create_problem():
    return {"message": "Problem created successfully"}


@router.post("/problem/CSES")
async def create_problem_cses():
    return {"message": "Problem created successfully"}
