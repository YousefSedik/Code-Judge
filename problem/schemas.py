from pydantic import BaseModel, field_validator
from typing import Optional, List
from fastapi import HTTPException


class ManualProblemAdd(BaseModel):
    title: str
    statement: str
    tutorial: Optional[str] = None
    time_limit: float  # in seconds
    memory_limit: int  # in MB
    input_test: List[str]
    output_test: List[str]

    @field_validator("output_test")
    def check_tests_length(cls, v, values):
        if "input_test" in values and len(values["input_test"]) != len(v):
            raise HTTPException(
                status_code=400,
                detail="input_test and output_test must be of the same size",
            )
        return v


class CSESProblemAdd(BaseModel):
    problem_id: int
