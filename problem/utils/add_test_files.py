import os
from problem.models import TestCase, Problem
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))[:-6]


async def add_test_files(
    problem: Problem,
    session: AsyncSession,
    input_tests: List[str],
    output_tests: List[str],
):
    problem_test_cases_dir = os.path.join(
        BASE_DIR, "problem_test_cases", str(problem.id)
    )
    os.makedirs(problem_test_cases_dir, exist_ok=True)

    for i in range(len(input_tests)):
        problem_test_case = TestCase(problem=problem)

        session.add(problem_test_case)
        await session.flush()

        input_file_path = problem_test_case.input_path
        output_file_path = problem_test_case.output_path

        with open(input_file_path, "w") as input_file:
            input_file.write(input_tests[i])
        with open(output_file_path, "w") as output_file:
            output_file.write(output_tests[i])
