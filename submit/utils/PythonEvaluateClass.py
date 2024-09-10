from submit.utils import EvaluateCode


class PythonEvaluate(EvaluateCode):

    def __init__(
        self,
        submission_id,
        source_code_path,
        output_testcase_file_path,
        input_testcase_file_path,
        time_limit_in_ms,
        memory_limit_in_mg,
    ):
        super().__init__(
            submission_id,
            source_code_path,
            output_testcase_file_path,
            input_testcase_file_path,
            time_limit_in_ms,
            memory_limit_in_mg,
        )

    async def evaluate(self):
        print(f"start evaluating python code for submission {self.submission_id}")
