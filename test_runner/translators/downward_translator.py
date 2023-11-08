import os.path

from ..test_case import TestCase

from .base_translator import BaseTranslator


downward_path = os.path.abspath("./test_runner/systems/downward/fast-downward.py")
class DownwardTranslator(BaseTranslator):
    def __init__(self, sample_count: int, searches: list["DownwardSearcher"] = []) -> None:
        super().__init__("downward", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None) -> str:
        translation_directory = self.get_translation_directory(test_case)

        return f"""\
"python3" \
"{os.path.relpath(downward_path, translation_directory)}" \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
"""

    def generate_translator_script_content(self, test_case: TestCase) -> str:

        return self._generate_translator_script_content_prefix(test_case) + f"""\
python3 -m venv venv
source venv/bin/activate

time {self.do_translation(test_case)}
"""
    

    def get_sas_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "output.sas"))
