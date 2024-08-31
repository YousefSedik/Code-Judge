from problem.schemas import ManualProblemAdd, CSESProblemAdd
from sqlalchemy.ext.asyncio import AsyncSession
from problem.models import Problem, TestCase, PROBLEM_SOURCE
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlmodel import select
from db import get_session
import os


router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@router.get("/problem/<problem_id>")
async def get_problem(problem_id: int, session: AsyncSession = Depends(get_session)):
    problem_info = await session.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem_info = problem_info.scalars().first()
    if problem_info is None:
        raise HTTPException("Problem not found", status_code=404)
    return problem_info.to_dict()


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

    problem_test_cases_dir = os.path.join(
        BASE_DIR, "problem_test_cases", str(problem.id)
    )
    os.makedirs(problem_test_cases_dir, exist_ok=True)

    for i in range(len(ManualProblemForm.input_test)):
        problem_test_case = TestCase(problem=problem)

        session.add(problem_test_case)
        await session.flush()

        input_file_path = problem_test_case.input_path
        output_file_path = problem_test_case.output_path

        with open(input_file_path, "w") as input_file:
            input_file.write(ManualProblemForm.input_test[i])
        with open(output_file_path, "w") as output_file:
            output_file.write(ManualProblemForm.output_test[i])

    await session.commit()

    return {"message": "Problem created successfully", "problem_id": problem.id}


@router.post("/problem/CSES")
async def create_problem_cses():
    return {"message": "Problem created successfully"}
