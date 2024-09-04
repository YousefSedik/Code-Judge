import os
from problem.models import TestCase, Problem
from sqlalchemy.ext.asyncio import AsyncSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))[:-6]


class WriteTestCases:
    def __init__(self, input_li, output_li, problem: Problem, session: AsyncSession):
        self.input_li = input_li
        self.output_li = output_li
        self.problem = problem
        self.session = session

    async def write_io_tests(self):

        problem_test_cases_dir = os.path.join(
            BASE_DIR, "problem_test_cases", str(self.problem.id)
        )
        os.makedirs(problem_test_cases_dir, exist_ok=True)

        for i in range(len(self.input_li)):
            problem_test_case = TestCase(problem=self.problem)

            self.session.add(problem_test_case)
            await self.session.flush()

            input_file_path = problem_test_case.input_path
            output_file_path = problem_test_case.output_path

            with open(input_file_path, "w") as input_file:
                input_file.write(self.input_li[i])
            with open(output_file_path, "w") as output_file:
                output_file.write(self.output_li[i])
