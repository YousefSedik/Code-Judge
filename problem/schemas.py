from pydantic import BaseModel
from typing import Optional, List


class ManualProblemAdd(BaseModel):
    title: str
    statement: str
    tutorial: Optional[str] = None
    time_limit: float  # in seconds
    memory_limit: int  # in MB
    input_test: List[str]
    output_test: List[str]


class CSESProblemAdd(BaseModel):
    problem_id: int
