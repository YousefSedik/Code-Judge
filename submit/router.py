from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from submit.models import Submission

# from auth.schemas import Token
# from auth.models import User
from auth.utils import get_current_user

from problem.models import Problem
from db import get_session
from submit.schemas import SubmitForm

router = APIRouter()


@router.post("/submit")
async def submit(
    token: str,
    SubmissionForm: SubmitForm,
    session: AsyncSession = Depends(get_session),
):

    user = await get_current_user(session, token)
    problem = await session.get(Problem, SubmissionForm.problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")

    submission = Submission(
        user_id=user.id,
        problem_id=SubmissionForm.problem_id,
        submission_language=SubmissionForm.submission_language,
        source_code=SubmissionForm.source_code,
    )
    session.add(submission)
    # Add Background task to judge the code
    # ...
    # ...

    await session.commit()
    await session.refresh(submission)

    return {"message": "Submission received", "submission_id": submission.id}
