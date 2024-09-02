from problem.schemas import ManualProblemAdd, CSESProblemAdd
from sqlalchemy.ext.asyncio import AsyncSession
from problem.models import Problem, PROBLEM_SOURCE, CSESProblemRequest
from fastapi import Depends, HTTPException, BackgroundTasks
from problem.utils import add_test_files, add_cses_problem
from fastapi.routing import APIRouter
from dotenv import load_dotenv
from sqlmodel import select
from db import get_session
import os


router = APIRouter()
load_dotenv(".env")


@router.get("/problem/{problem_id}")
async def get_problem(problem_id: int, session: AsyncSession = Depends(get_session)):
    problem_info = await session.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem_info = problem_info.scalars().first()

    if problem_info is None:
        raise HTTPException(detail="Problem not found", status_code=404)
    return problem_info


@router.post("/problem/manual")
async def create_problem_manual(
    ManualProblemForm: ManualProblemAdd, session: AsyncSession = Depends(get_session)
):
    # Create the problem object
    problem = Problem(
        source=PROBLEM_SOURCE.MANUAL,
        title=ManualProblemForm.title,
        statement=ManualProblemForm.statement,
        tutorial=ManualProblemForm.tutorial,
        time_limit=ManualProblemForm.time_limit,
        memory_limit=ManualProblemForm.memory_limit,
    )

    session.add(problem)
    await session.flush()
    await add_test_files(
        problem,
        session,
        ManualProblemForm.input_test,
        ManualProblemForm.output_test,
    )
    await session.commit()

    return {"message": "Problem created successfully", "problem_id": problem.id}


@router.post("/problem/CSES")
async def create_problem_cses(
    CSESProblemForm: CSESProblemAdd,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    cses_problem_id = CSESProblemForm.problem_id

    problem_request = CSESProblemRequest(cses_problem_id=cses_problem_id)
    session.add(problem_request)
    await session.commit()
    await session.refresh(problem_request)

    PHPSESSID = os.getenv("PHPSESSID")
    if not PHPSESSID:
        raise HTTPException(
            status_code=500, detail="PHPSESSID environment variable not set"
        )
    background_tasks.add_task(
        add_cses_problem, cses_problem_id, problem_request.id, PHPSESSID, session
    )

    return {"request_id": problem_request.id}


@router.get("/problem/CSES/request/{request_id}")
async def get_cses_request(
    request_id: int, session: AsyncSession = Depends(get_session)
):
    request_info = await session.execute(
        select(CSESProblemRequest).where(CSESProblemRequest.id == request_id)
    )
    request_info = request_info.scalars().first()
    if request_info is None:
        raise HTTPException(detail="Request not found", status_code=404)
    return request_info
