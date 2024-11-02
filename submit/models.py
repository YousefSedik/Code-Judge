from sqlmodel import Field, SQLModel, Relationship
from problem.models import Problem
from typing import Optional, List
from datetime import datetime
from sqlalchemy import event
from enum import Enum
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SUBMISSION_LANGUAGE(str, Enum):
    CPP = "C++"
    PY = "Python"


class SUBMISSION_VERDICT(str, Enum):
    AC = "Accepted"
    WA = "Wrong Answer"
    TLE = "Time Limit Exceeded"
    MEME = "Memory Limit Exceeded"
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
            f"submissions/{self.id}/source_code.{file_extension}",
        )

    def __str__(self):
        return f"Submission {self.id} by {self.user.username} for {self.problem.title}"


def after_save(mapper, connection, target):
    path = target.source_code_path
    os.makedirs(os.path.join(BASE_DIR, f"submissions/{target.id}"), exist_ok=True)
    # create a file with the source code
    os.system(f"touch {path}")
    with open(path, "w") as file:
        file.write(target.source_code)


event.listen(Submission, "after_insert", after_save)
