import os.path

from ..test_case import TestCase

from .base_translator import BaseTranslator


translator_path = os.path.abspath("./test_runner/systems/tapaal-4xx/lib/tapaal.jar") # TODO: Fix when submodule installed
class CPNTranslator(BaseTranslator):
    def __init__(self, sample_count: int, searches: list["CPNTranslator"] = []) -> None:
        super().__init__("cpn", sample_count, searches)


    def do_translation(self, test_case: "TestCase") -> str:
        translation_directory = self.get_translation_directory(test_case)

# TODO: Fix when submodule installed, queries instead of problem?
        return f"""\
"java" \
"{os.path.relpath(translator_path, translation_directory)}" \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
""" 

    def generate_translator_script_content(self, test_case: TestCase) -> str:

        return self._generate_translator_script_content_prefix(test_case) + f"""\
time {self.do_translation(test_case)}
"""
    
