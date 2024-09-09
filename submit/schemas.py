from pydantic import BaseModel, field_validator
from submit.models import SUBMISSION_LANGUAGE
from problem.models import Problem
from sqlmodel import select


class SubmitForm(BaseModel):
    source_code: str
    submission_language: SUBMISSION_LANGUAGE
    problem_id: int
