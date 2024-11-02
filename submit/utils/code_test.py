from submit.utils import PythonEvaluate
from submit.utils import CPPEvaluate
from submit.models import Submission, SUBMISSION_LANGUAGE, SUBMISSION_VERDICT
from problem.models import Problem, TestCase
from typing import List
from db import AsyncSessionLocal
from sqlmodel import select
import os


def compile_cpp(source_code_path: str) -> bool:
    print("start compiling C++ code for submission")
    compiled_file_path = source_code_path.split(".")[0] + ".out"
    exit_code = os.system(
        f"g++ {source_code_path} -o {compiled_file_path} "
    )
    if exit_code == 0:
        print("C++ code compiled successfully")
        return True, compiled_file_path
    print("C++ code compilation failed")
    return False, None


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
        if submission.submission_language == SUBMISSION_LANGUAGE.CPP:
            is_compiled, compiled_file_path = compile_cpp(
                    submission.source_code_path
                )
            if not is_compiled:
                submission.verdict = SUBMISSION_VERDICT.CE
                session.add(submission)
                await session.commit()
                return 
        try:
            if submission.submission_language == SUBMISSION_LANGUAGE.CPP:
                for testcase in test_cases:
                    result = await CPPEvaluate(
                        submission.id,
                        compiled_file_path,
                        testcase.input_path,
                        testcase.output_path,
                        problem.time_limit,
                        problem.memory_limit,
                    ).evaluate()
                    if result != SUBMISSION_VERDICT.AC:
                        break
                
                if result != SUBMISSION_VERDICT.AC:
                    submission.verdict = result
                    session.add(submission)
                    await session.commit()
                    # stop. no need to evaluate further test cases
                    return

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

            # all test cases passed successfully. verdict is AC
            submission.verdict = SUBMISSION_VERDICT.AC
            session.add(submission)
            await session.commit()
            print("Evaluation done")
            return 
        except Exception as e:
            print(e)
