from ..analysers import *
from .. import TestCase
from . import *


class DoNothingTranslator(BaseTranslator):
    def __init__(self, sample_count: int, searches: list["BaseSearcher"] = []) -> None:
        super().__init__("nothing", sample_count, searches)

    def generate_translator_script_content(self, test_case: TestCase) -> str:
        return self._generate_translator_script_content_prefix(test_case) + "time echo"
    
    def get_petrinet_path(self, test_case: TestCase):
        return test_case.domain_path

    def get_query_path(self, test_case: "TestCase"):
        return test_case.problem_path
    