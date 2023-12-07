import os
import glob

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


    def do_searches(self, translator: "BaseTranslator", test_case: "TestCase") -> str:
        out: list[str] = []
        for i in range(self.sample_count):
            out.append(self.do_search(translator, test_case, i))
        
        return "\n".join(out)


    def do_search(self, translator: "BaseTranslator", test_case: "TestCase") -> None:
        pass


    def get_result_paths(self, translator: "BaseTranslator", test_case: "TestCase") -> list[str]:
        base_path = os.path.join(translator.base_dir, translator.name, test_case.name, self.name)
        return glob.glob(f"{base_path}/*.search.*.txt")


    def parse_results(self, translator: "BaseTranslator",  test_case: "TestCase") -> list["SearchResult"]:
        return [self.parser().parse(result_path) for result_path in self.get_result_paths(translator, test_case)]


    def _generate_search_script_content_base(self, translator: BaseTranslator, test_case: TestCase) -> str:
        return f"""\
#!/bin/bash
#SBATCH -J "{translator.name} - {test_case.name} - {self.name}"
#SBATCH --mail-type=FAIL  # BEGIN,END,FAIL,ALL,NONE
#SBATCH --mail-user=hginne19@student.aau.dk
#SBATCH --partition=naples,dhabi
#SBATCH --time=1:00:00
#SBATCH --mem=16G

let "m=1024*1024*15"
ulimit -v $m

"""
    
    
    def generate_search_script_content(self, translator: BaseTranslator, test_case: TestCase) -> str:
        pass
    