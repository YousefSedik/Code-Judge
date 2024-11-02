from submit.utils import EvaluateCode
import os
from submit.models import SUBMISSION_VERDICT


class CPPEvaluate(EvaluateCode):

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
        time_limit = 1 # seconds
        mem_limit = 512 # mg
        run_command = f"ulimit -v {mem_limit * 1024}; ./code"
        create_bwrap_instance = f"""
                bwrap \
                --ro-bind /usr /usr \
                --ro-bind /lib /lib \
                --ro-bind /lib64 /lib64 \
                --proc /proc \
                --dev /dev \
                --dir /tmp \
                --unshare-pid \
                --unshare-net \
                --dir /sandbox \
                --bind {self.source_code_path} /code \
                --bind {self.input_testcase_file_path} /input \
                --bind {self.output_testcase_file_path} /output \
                --setenv PATH /usr/local/bin:/usr/bin \
                /usr/bin/bash -c " {run_command}"
        """
        # print(create_bwrap_instance)

        exit_code = os.system(create_bwrap_instance)
        print("Exit Code: ", exit_code)
        if exit_code == -9:
            return SUBMISSION_VERDICT.MEME
        if exit_code != 0:
            return SUBMISSION_VERDICT.RE
        # check if time limit exceeded?
        # check if memory limit exceeded?
        return SUBMISSION_VERDICT.AC
