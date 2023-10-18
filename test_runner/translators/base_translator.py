import os.path

from ..analysers import *
from .. import TestCase
from . import *


class BaseTranslator(object):
    name: str
    sample_count: int
    searchers: list["BaseSearcher"]
    base_dir: str = "./experiments/"
    parser: TranslatorResult = TranslatorResult

    def __init__(self, name: str, sample_count: int, searchers: list["BaseSearcher"]) -> None:
        self.name = name
        self.sample_count = sample_count
        self.searchers = searchers


    def do_translations_and_searches(self, test_cases: list[TestCase]):
        for case in test_cases:
            for i in range(self.sample_count):
                self.do_translation(case, i)
            
            for search in self.searchers:
                search.do_searches(self, case)


    def do_translations(self, test_cases: list[TestCase]):
        for case in test_cases:
            for i in range(self.sample_count):
                self.do_translation(case, i)
    

    def do_searches(self, test_cases: list[TestCase]):
        for case in test_cases:
            for search in self.searchers:
                search.do_searches(self, case)


    def do_translation(self, test_case: TestCase, iterator: int = None):
        pass


    def get_translation_directory(self, test_case: TestCase) -> str:
        dir = os.path.join(self.base_dir, self.name, test_case.name)
        os.makedirs(dir, exist_ok=True)
        return dir


    def get_result_paths(self) -> tuple[str, str]:
        return [(self.get_result_path(i), self.get_result_time_path(i)) for i in range(self.sample_count)]


    def get_result_path(self, test_case: "TestCase", iterator: int):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), f"result_translation_{iterator}.txt"))
        

    def get_result_time_path(self, test_case: "TestCase", iterator: int):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), f"result_translation_time_{iterator}.txt"))
    

    def parse_results(self, test_cases: list["TestCase"]) -> dict["TestCase", list[TranslatorResult]]:
        results: dict["TestCase", list[TranslatorResult]] = dict()
        for case in test_cases:
            results[case] = [
                TranslatorResult().parse_files(
                    self.get_result_path(case, i),
                    self.get_result_time_path(case, i),
                    ) 
                for i in range(self.sample_count)
            ]
        
        return results


    def parse_search_results(self, test_cases: list["TestCase"]) -> dict["TestCase", dict["BaseSearcher", list["SearchResult"]]]:
        result: dict["TestCase", dict["BaseSearcher", list["SearchResult"]]] = dict()

        for case in test_cases:
            result[case] = dict()
            for searcher in self.searchers:
                result[case][searcher] = searcher.parse_results(self, case)

        return result

