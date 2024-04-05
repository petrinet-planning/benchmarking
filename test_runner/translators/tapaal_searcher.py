import os.path

from ..analysers import TapaalResult, TapaalSimpleResult
from ..test_case import TestCase

from . import *

class TapaalSearcher(BaseSearcher):
    parameters: list[str]
    engine_path: str
    parser: TapaalResult = TapaalSimpleResult


    def __init__(self, engine_path: str, name: str, sample_count: int, parameters: list[str] = []) -> None:
        super().__init__(name, sample_count)
        self.engine_path = engine_path
        self.parameters = parameters


    def do_search(self, translator: "TapaalTranslator", test_case: "TestCase") -> str:
        translator_working_directory = translator.get_translation_directory(test_case)
        petrinet_path = os.path.relpath(translator.get_petrinet_path(test_case), translator_working_directory)
        query_path = os.path.relpath(translator.get_query_path(test_case), translator_working_directory)

        param_str = "" if len(self.parameters)==0 else f'''"{'" "'.join(self.parameters)}"'''

        return f"""\
"{self.engine_path}" \
{param_str} \
"{petrinet_path}" \
"{query_path}" \
"""
    
    
    def generate_search_script_content(self, translator: BaseTranslator, test_case: TestCase) -> str:
        return self._generate_search_script_content_base(translator, test_case) + f"""\

time {self.do_search(translator, test_case)}
"""
    