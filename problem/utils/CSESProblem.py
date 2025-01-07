from bs4 import BeautifulSoup
from requests import Session
from pylatexenc.latex2text import LatexNodes2Text

# from zipfile import ZipFile
from lxml import etree
import os
from problem.utils.ReadTests import ReadTestCases

BASE_DIR = os.path.dirname(os.path.abspath(__file__))[0:-6]


class CSESProblem:
    __title_xpath = "/html/body/div[2]/div[1]/div[1]/h1"
    __time_limit_xpath = "/html/body/div[2]/div[2]/div[1]/ul/li[1]/text()"
    __memory_limit_xpath = "/html/body/div[2]/div[2]/div[1]/ul/li[2]/text()"
    __statement_xpath = "/html/body/div[2]/div[2]/div[1]/div/p[1]"

    def __init__(self, problem_id: str, PHPSESSID: str):
        self.__cses_session = Session()
        self.__cses_session.cookies.set("PHPSESSID", PHPSESSID)
        self.__problem_id = problem_id
        self.__problem_url = f"https://cses.fi/problemset/task/{problem_id}"
        self.__download_tests_url = f"https://cses.fi/problemset/tests/{problem_id}/"
        self.__tests_response = self.__cses_session.get(self.__download_tests_url)
        if "CSES Problem Set" not in self.__tests_response.text:
            raise Exception("Problem not found in CSES")
        self.__problem_response = self.__cses_session.get(self.__problem_url)
        self.__problem_response_bs4 = BeautifulSoup(
            self.__problem_response.text, "html.parser"
        )
        self.__tests_response_bs4 = BeautifulSoup(
            self.__tests_response.text, "html.parser"
        )
        self.__problem_dom = etree.HTML(str(self.__problem_response_bs4))
        self.title = self.__problem_dom.xpath(self.__title_xpath)[0].text
        self.time_limit = self.__problem_dom.xpath(self.__time_limit_xpath)[0].split(
            " "
        )[1]
        self.memory_limit = self.__problem_dom.xpath(self.__memory_limit_xpath)[
            0
        ].split(" ")[1]
        self.statement = LatexNodes2Text().latex_to_text(
            latex=self.__problem_response_bs4.find("div", {"class": "md"}).text
        )

    def __get_tests(self):
        problem_id = self.__problem_id
        csrf_token = self.__tests_response_bs4.find(
            "input", {"name": "csrf_token"}
        ).get("value")
        data = {"csrf_token": csrf_token, "download": "true"}
        response = self.__cses_session.post(
            self.__download_tests_url, data=data, stream=True
        )
        with open(f"{problem_id}.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        read_test_cases = ReadTestCases(problem_id)
        input_tests, output_tests = read_test_cases.read_io_tests()
        # print(input_tests, output_tests)
        return input_tests, output_tests

    def __dict__(self):
        input_tests, output_tests = self.__get_tests()
        return {
            "title": self.title,
            "statement": self.statement,
            "time_limit": float(self.time_limit),
            "memory_limit": int(self.memory_limit),
            "input_test": input_tests,
            "output_test": output_tests,
        }

    def to_dict(self):
        return self.__dict__()
