from sqlmodel import Field, SQLModel, Relationship, SmallInteger
from typing import Optional, List
from enum import Enum


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
    test_cases: Optional[List["TestCase"]] = Relationship(back_populates="problem")


class TestCase(SQLModel, table=True):
    id: int = Field(primary_key=True)
    problem: Problem = Relationship(back_populates="test_cases")

    @property
    def input_path(self):
        return f"/app/problem/problem_test_cases/{self.problem.id}/input-{self.id}.txt"

    @property
    def output_path(self):
        return f"/app/problem/problem_test_cases/{self.problem.id}/output-{self.id}.txt"

    def __str__(self):
        return f"Test case {self.id}"
