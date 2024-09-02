from zipfile import ZipFile
import os


class ReadTestCases:
    def __init__(self, problem_id):
        self.problem_id = problem_id

    def read_io_tests(self):
        problem_id = self.problem_id
        input_tests = []
        output_tests = []
        with ZipFile(f"{problem_id}.zip", "r") as zip_ref:
            zip_ref.extractall(f"{problem_id}")
            tests = os.listdir(f"{problem_id}")
            test_count = len(tests) // 2
            for i in range(test_count):
                input_tests.append(open(f"{problem_id}/{i + 1}.in").read())
                output_tests.append(open(f"{problem_id}/{i + 1}.out").read())

            os.remove(f"{problem_id}.zip")
            self.rmdir(f"{problem_id}")
        return input_tests, output_tests

    @staticmethod
    def rmdir(dir: str):
        if os.path.exists(f"{dir}"):
            for root, dirs, files in os.walk(f"{dir}", topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(f"{dir}")
