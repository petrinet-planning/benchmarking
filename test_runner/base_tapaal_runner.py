

import time

from .base_test_runner import BaseTestRunner
from .test_case import TestCase
from .translation_result import TranslationResult
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

    def run(self, test_case: TestCase, iterator: int = None) -> QueryResult:

        time_translation = time.time()
        self.do_translation(test_case, iterator)
        time_translation = time.time() - time_translation

        time_tapaal = time.time()
        tapaal_stdout_full = self.do_planning(test_case, iterator)
        time_tapaal = time.time() - time_tapaal

        query_output_parsed = QueryResult.parse(tapaal_stdout_full)

        query_output_parsed.time_translation = time_translation
        query_output_parsed.time_tapaal = time_tapaal
        query_output_parsed.time_total = time_translation + time_tapaal

        return query_output_parsed
    