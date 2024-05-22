import os.path

from ..test_case_c2p import TestCase_c2p

from .base_translator import BaseTranslator
from .enhsp_searcher import ENHSPSearcher

class CpnToPddlTranslator(BaseTranslator):
    translator_path: str
    _rel_pddl_out_dir: str = "out"

    def __init__(self, translator_path: str, sample_count: int, searches: list["ENHSPSearcher"] = []) -> None:
        super().__init__("cpn", sample_count, searches)
        self.translator_path = translator_path

    def do_translation(self, test_case: "TestCase_c2p") -> str:
        translation_directory = self.get_translation_directory(test_case)

        pddl_out_path = os.path.join(translation_directory, self._rel_pddl_out_dir)

        return f"""\
"{os.path.relpath(self.translator_path, translation_directory)}" \
-pddl-out "{os.path.relpath(pddl_out_path, translation_directory)}" \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
""" 

    def generate_translator_script_content(self, test_case: TestCase_c2p) -> str:

        return self._generate_translator_script_content_prefix(test_case) + f"""\
time {self.do_translation(test_case)}
"""
    
    def get_model_path(self, test_case: "TestCase_c2p") -> str:
        translation_directory = self.get_translation_directory(test_case)

        pddl_out_path = os.path.join(translation_directory, self._rel_pddl_out_dir)
        domain_path = os.path.join(pddl_out_path, "model.pddl")

        return domain_path

    def get_query_path(self, test_case: "TestCase_c2p") -> str:
        translation_directory = self.get_translation_directory(test_case)

        pddl_out_path = os.path.join(translation_directory, self._rel_pddl_out_dir)
        problem_path = os.path.join(pddl_out_path, test_case.query_name + ".pddl")

        return problem_path
