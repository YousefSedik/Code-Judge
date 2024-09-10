from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from enum import Enum
import os
from datetime import datetime
from sqlmodel import Relationship

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class PROBLEM_SOURCE(str, Enum):
    MANUAL = "Manual"
    CSES = "cses"


class Problem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    source: PROBLEM_SOURCE = Field(nullable=False)
    title: str = Field(nullable=False)
    statement: str = Field(nullable=False)
    tutorial: Optional[str] = None
    time_limit: Optional[float]  # in seconds
    memory_limit: Optional[int]  # in MB
    test_cases: List["TestCase"] = Relationship(back_populates="problem")
    submissions: Optional[List["Submission"]] = Relationship(back_populates="problem")


class TestCase(SQLModel, table=True):
    id: int = Field(primary_key=True)
    problem_id: Optional[int] = Field(foreign_key="problem.id", nullable=False)
    problem: Problem = Relationship(back_populates="test_cases")

    @property
    def input_path(self):
        return os.path.join(
            BASE_DIR,
            f"problem_test_cases/{self.problem_id}/input-{self.id}.txt",
        )

    @property
    def output_path(self):
        return os.path.join(
            BASE_DIR,
            f"problem_test_cases/{self.problem_id}/output-{self.id}.txt",
        )

    def __str__(self):
        return f"Test case {self.id}"


class PROBLEM_REQUEST_STATUS(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    FAILED = "Failed"


class CSESProblemRequest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    status: PROBLEM_REQUEST_STATUS = Field(
        nullable=False, default=PROBLEM_REQUEST_STATUS.PENDING
    )
    problem_id: Optional[int] = Field(foreign_key="problem.id", nullable=True)
    cses_problem_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    error_msg: Optional[str] = None
