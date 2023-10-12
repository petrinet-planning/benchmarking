

import time
from . import BaseTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query, QueryResult, Engine


class BaseTapaalTestRunner(BaseTestRunner):
    tapaal_engine: Engine
    description: str
    base_parameters: list[str]

    def __init__(self, translation_name: str, description: str, needed_sample_size: int, tapaal_engine_path: str, base_parameters: list[str] = []):
        super().__init__(translation_name, description, needed_sample_size)
        self.tapaal_engine = Engine(tapaal_engine_path)
        self.base_parameters = base_parameters

    def run(self, test_case: TestCase) -> QueryResult:

        translation_time = time.time()
        self.do_translation(test_case)
        translation_time = time.time() - translation_time

        tapaal_time = time.time()
        tapaal_stdout_full = self.do_tapaal()
        tapaal_time = time.time() - tapaal_time

        query_output_parsed = QueryResult.parse(tapaal_stdout_full)

        query_output_parsed.translation_time = translation_time
        query_output_parsed.tapaal_time = tapaal_time

        return query_output_parsed
    
    def do_translation(self, test_case: TestCase) -> None:
        raise Exception("Not implemented for base class")

    def do_tapaal(self):
        raise Exception("Not implemented for base class")

