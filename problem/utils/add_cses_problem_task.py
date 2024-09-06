from problem.utils import CSESProblem
from problem.models import (
    CSESProblemRequest,
    PROBLEM_REQUEST_STATUS,
    Problem,
    PROBLEM_SOURCE,
)
from sqlmodel import update, select
from problem.utils.WriteTests import WriteTestCases
from db import AsyncSessionLocal


async def add_cses_problem(cses_problem_id: int, request_id: int, PHPSESSID: str):
    async with AsyncSessionLocal() as session:
        try:
            # Check if the problem already exists
            result = await session.execute(
                select(CSESProblemRequest).where(
                    CSESProblemRequest.cses_problem_id == cses_problem_id,
                    CSESProblemRequest.status == PROBLEM_REQUEST_STATUS.ACCEPTED,
                )
            )
            already_exists = result.scalars().first()
            if already_exists:
                raise Exception("Problem already exists")

            # Fetch the CSES problem data
            cses_problem = CSESProblem(cses_problem_id, PHPSESSID)
            cses_problem = cses_problem.to_dict()

            # Create a new Problem entry
            problem = Problem(
                source=PROBLEM_SOURCE.CSES,
                title=cses_problem["title"],
                statement=cses_problem["statement"],
                time_limit=cses_problem["time_limit"],
                memory_limit=cses_problem["memory_limit"],
            )
            session.add(problem)
            await session.flush()

            # Write the test cases
            write_tests = WriteTestCases(
                cses_problem["input_test"],
                cses_problem["output_test"],
                problem,
                session,
            )
            await write_tests.write_io_tests()

            # Update the problem request to accepted
            await session.execute(
                update(CSESProblemRequest)
                .where(CSESProblemRequest.id == request_id)
                .values(status=PROBLEM_REQUEST_STATUS.ACCEPTED, problem_id=problem.id)
            )
            await session.commit()

        except Exception as e:
            await session.rollback()

            # Update the problem request to failed
            await session.execute(
                update(CSESProblemRequest)
                .where(CSESProblemRequest.id == request_id)
                .values(status=PROBLEM_REQUEST_STATUS.FAILED, error_msg=str(e))
            )
            await session.commit()
