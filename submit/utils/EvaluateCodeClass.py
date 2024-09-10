from abc import ABC
import os
from abc import ABC, abstractmethod


class EvaluateCode(ABC):

    def __init__(
        self,
        submission_id,
        source_code_path,
        output_testcase_file_path,
        input_testcase_file_path,
        time_limit_in_ms,
        memory_limit_in_mg,
    ):
        self.submission_id = submission_id
        self.source_code_path = source_code_path
        self.output_testcase_file_path = output_testcase_file_path
        self.input_testcase_file_path = input_testcase_file_path
        self.time_limit_in_ms = time_limit_in_ms
        self.memory_limit_in_mg = memory_limit_in_mg

    @abstractmethod
    async def evaluate(self):
        pass
