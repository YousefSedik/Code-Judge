from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from submit.models import Submission
from submit.utils.code_evaluate import test
from auth.utils import get_current_user
from problem.models import Problem, TestCase
from db import get_session
from submit.schemas import SubmitForm
from sqlmodel import select
from submit.tasks import task_code_task
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/submit")
async def submit(
    SubmissionForm: SubmitForm,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):

    user = await get_current_user(session, token)
    problem = await session.get(Problem, SubmissionForm.problem_id)

    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    source_code = ""
    for line in SubmissionForm.source_code:
        source_code += line + "\n"

    submission = Submission(
        user_id=user.id,
        problem_id=SubmissionForm.problem_id,
        submission_language=SubmissionForm.submission_language,
        source_code=source_code,
    )

    session.add(submission)
    await session.commit()
    await session.refresh(submission)
    task_code_task.delay(submission.id, problem.id)
    return {"message": "Submission received", "submission_id": submission.id}


@router.get("/submission/{submission_id}")
async def get_submission(
    submission_id: int, session: AsyncSession = Depends(get_session)
):
    submission = await session.get(Submission, submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {
        "id": submission.id,
        "problem_id": submission.problem_id,
        "submission_language": submission.submission_language,
        "source_code": submission.source_code.split("\n"),
        "verdict": submission.verdict,
        "created_at": submission.created_at,
        "user_id": submission.user_id,
    }
