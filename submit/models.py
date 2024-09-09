from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from enum import Enum
import os
from datetime import datetime
from problem.models import Problem

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SUBMISSION_LANGUAGE(str, Enum):
    CPP = "C++"
    PY = "Python"


class SUBMISSION_VERDICT(str, Enum):
    AC = "Accepted"
    WA = "Wrong Answer"
    TLE = "Time Limit Exceeded"
    RE = "Runtime Error"
    CE = "Compilation Error"
    PI = "Pending"


class Submission(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="submissions")

    problem_id: int = Field(foreign_key="problem.id", nullable=False)
    problem: Problem = Relationship(back_populates="submissions")
    submission_language: SUBMISSION_LANGUAGE = Field(nullable=False)
    source_code: str = Field(nullable=False)
    verdict: SUBMISSION_VERDICT = Field(nullable=False, default=SUBMISSION_VERDICT.PI)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def source_code_path(self):
        file_extension = None
        if self.submission_language == SUBMISSION_LANGUAGE.CPP:
            file_extension = "cpp"

        elif self.submission_language == SUBMISSION_LANGUAGE.PY:
            file_extension = "py"

        if file_extension is None:
            raise ValueError("Invalid submission language")

        return os.path.join(
            BASE_DIR,
            f"submit/submissions/{self.id}/source_code.{file_extension}",
        )

    def __str__(self):
        return f"Submission {self.id} by {self.user.username} for {self.problem.title}"
