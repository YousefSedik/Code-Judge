from submit.utils import PythonEvaluate
from submit.utils import CPPEvaluate
from submit.models import Submission, SUBMISSION_LANGUAGE
from problem.models import Problem, TestCase
from typing import List
from db import AsyncSessionLocal
from sqlmodel import select


# background task
async def test(
    submission: Submission,
    problem: Problem,
):
    async with AsyncSessionLocal() as session:
        result: list[TestCase] = await session.execute(
            select(TestCase).where(TestCase.problem_id == problem.id)
        )
        test_cases = result.scalars().all()
        try:
            if submission.submission_language == SUBMISSION_LANGUAGE.CPP:
                for testcase in test_cases:
                    await CPPEvaluate(
                        submission.id,
                        submission.source_code_path,
                        testcase.input_path,
                        testcase.output_path,
                        problem.time_limit,
                        problem.memory_limit,
                    ).evaluate()
            elif submission.submission_language == SUBMISSION_LANGUAGE.PY:
                for testcase in test_cases:
                    await PythonEvaluate(
                        submission.id,
                        submission.source_code_path,
                        testcase.input_path,
                        testcase.output_path,
                        problem.time_limit,
                        problem.memory_limit,
                    ).evaluate()
            else:
                raise ValueError("Invalid submission language")

            print("Evaluation done")
        except Exception as e:
            print(e)
