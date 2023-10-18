from ..analysers import SearchResult
from ..test_case import TestCase
from . import *


class BaseSearcher(object):
    name: str
    sample_count: int
    parser: SearchResult = SearchResult

    def __init__(self, name: str, sample_count: int) -> None:
        self.name = name
        self.sample_count = sample_count


    def do_searches(self, translator: "BaseTranslator", test_case: "TestCase") -> None:
        for i in range(self.sample_count):
            self.do_search(translator, test_case, i)


    def do_search(self, translator: "BaseTranslator", test_case: "TestCase", iterator: int = None) -> None:
        pass


    def get_result_paths(self, test_cases: list["TestCase"]) -> tuple[str, str]:
        return [(self.get_result_path(case, i), self.get_result_time_path(case, i)) for i in self.sample_count for case in test_cases]


    def get_result_path(self, iterator: int):
        return f"result_translation_{iterator}.txt",
        

    def get_result_time_path(self, iterator: int):
        return f"result_translation_time_{iterator}.txt"

    def parse_results(self, translator: "BaseTranslator",  test_case: "TestCase") -> list["SearchResult"]:
        return [
            self.parser().parse_files(
                self.get_result_path(translator, test_case, i), 
                self.get_result_time_path(translator, test_case, i)
                )
            for i in range(self.sample_count)
        ]
        