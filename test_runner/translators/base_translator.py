import os.path
import glob

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
        out: list[str] = []

        for case in test_cases:
            for i in range(self.sample_count):
                out.append(self.do_translation(case, i))
            
            for search in self.searchers:
                out.append(search.do_searches(self, case))

        return "\n".join(out)

    def do_translations(self, test_cases: list[TestCase]) -> str:
        translations:list[str] = []
        for case in test_cases:
            for i in range(self.sample_count):
                translations.append(self.do_translation(case, i))
    
        return "\n".join(translations)
    

    def do_searches(self, test_cases: list[TestCase]):
        searches:list[str] = []

        for case in test_cases:
            for search in self.searchers:
                searches.append(search.do_searches(self, case))
        return "\n".join(searches)


    def do_translation(self, test_case: TestCase, iterator: int = None):
        pass


    def get_translation_directory(self, test_case: TestCase) -> str:
        dir = os.path.join(self.base_dir, self.name, test_case.name)
        os.makedirs(dir, exist_ok=True)
        return dir
    
    def _generate_translator_script_content_prefix(self, test_case: TestCase) -> str:
        return f"""\
#!/bin/bash
#SBATCH -J "{self.name} - {test_case.name} - translation"
#SBATCH --mail-type=FAIL  # BEGIN,END,FAIL,ALL,NONE
#SBATCH --mail-user=hginne19@student.aau.dk
#SBATCH --partition=dhabi
#SBATCH --time=1:00:00
#SBATCH --mem=16G

let "m=1024*1024*15"
ulimit -v $m

"""
    
    def generate_translator_script_content(self, test_case: TestCase) -> str:
        pass


    def get_result_paths(self, test_case: "TestCase") -> list[str]:
        base_path = os.path.join(self.base_dir, self.name, test_case.name)
        return glob.glob(f"{base_path}/*.translation.*.txt")
    

    def parse_results(self, test_cases: list["TestCase"]) -> dict["TestCase", list[TranslatorResult]]:
        results: dict["TestCase", list[TranslatorResult]] = dict()

        for case in test_cases:
            results[case] = [TranslatorResult().parse(result_path) for result_path in self.get_result_paths(case)]
        
        return results


    def parse_search_results(self, test_cases: list["TestCase"]) -> dict["TestCase", dict["BaseSearcher", list["SearchResult"]]]:
        result: dict["TestCase", dict["BaseSearcher", list["SearchResult"]]] = dict()

        for case in test_cases:
            result[case] = dict()
            for searcher in self.searchers:
                result[case][searcher] = searcher.parse_results(self, case)

        return result

