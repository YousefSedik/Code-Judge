from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from submit.models import Submission
from submit.utils.code_test import test

# from auth.schemas import Token
# from auth.models import User
from auth.utils import get_current_user
from fastapi import BackgroundTasks
from problem.models import Problem, TestCase
from db import get_session
from submit.schemas import SubmitForm
from sqlmodel import select

router = APIRouter()


@router.post("/submit")
async def submit(
    token: str,
    SubmissionForm: SubmitForm,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):

    user = await get_current_user(session, token)
    problem = await session.get(Problem, SubmissionForm.problem_id)
    print(problem.time_limit, problem.memory_limit)

    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    submission = Submission(
        user_id=user.id,
        problem_id=SubmissionForm.problem_id,
        submission_language=SubmissionForm.submission_language,
        source_code=SubmissionForm.source_code,
    )

    session.add(submission)
    await session.commit()
    await session.refresh(submission)

    background_tasks.add_task(test, submission, problem)

    return {"message": "Submission received", "submission_id": submission.id}
