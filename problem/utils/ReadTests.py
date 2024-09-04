from zipfile import ZipFile
import os


class ReadTestCases:
    def __init__(self, problem_id, zip_file_name=None):
        if zip_file_name is None:
            zip_file_name = f"{problem_id}"

        self.zip_file_name = zip_file_name
        self.problem_id = problem_id

    def read_io_tests(self):
        input_tests = []
        output_tests = []
        with ZipFile(f"{self.zip_file_name}.zip", "r") as zip_ref:
            zip_ref.extractall(f"{self.zip_file_name}")
            tests = os.listdir(f"{self.zip_file_name}")
            test_count = len(tests) // 2
            for i in range(test_count):
                input_tests.append(open(f"{self.zip_file_name}/{i + 1}.in").read())
                output_tests.append(open(f"{self.zip_file_name}/{i + 1}.out").read())

            os.remove(f"{self.zip_file_name}.zip")
            self.rmdir(f"{self.zip_file_name}")
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
