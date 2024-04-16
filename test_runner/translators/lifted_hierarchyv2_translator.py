import os.path

from ..test_case import TestCase

from .tapaal_translator import TapaalTranslator


colored_hierarchy_translation_path = os.path.abspath("./test_runner/systems/type_hierarchy_v2/main.py")
class LiftedHierarchyV2Translator(TapaalTranslator):
    def __init__(self, sample_count: int, searches: list["TapaalColorSearcher"] = []) -> None:
        super().__init__("colored_hierarchyv2", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None) -> str:
        translation_directory = self.get_translation_directory(test_case)
        petrinet_path = self.get_petrinet_path(test_case)
        petrinet_query_path = self.get_query_path(test_case)

        return f"""\
"python3" \
"{os.path.relpath(colored_hierarchy_translation_path, translation_directory)}" \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
"{os.path.relpath(petrinet_path, translation_directory)}" \
"{os.path.relpath(petrinet_query_path, translation_directory)}" \
"""


    def generate_translator_script_content(self, test_case: TestCase) -> str:

        return self._generate_translator_script_content_prefix(test_case) + f"""\
source ../colored_venv/bin/activate

time {self.do_translation(test_case)}
"""

    def get_petrinet_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "petrinet.pnml"))


    def get_query_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "query.pnml"))
    
