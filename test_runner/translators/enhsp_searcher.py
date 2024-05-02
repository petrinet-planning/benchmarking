import os.path

from ..analysers import CPNSearchResult
from ..test_case import TestCase

from . import *

class ENHSPSearcher(BaseSearcher):
    parameters: list[str]
    engine_path: str
    parser: CPNSearchResult = CPNSearchResult

    def __init__(self, engine_path: str, name: str, sample_count: int, parameters: list[str] = []) -> None:
        super().__init__(name, sample_count)
        self.engine_path = engine_path
        self.parameters = parameters
    
    
    def out_dir(self, translator: "CPNTranslator", test_case: "TestCase"):
        dir = os.path.join(translator.get_translation_directory(test_case), self.name)
        os.makedirs(dir, exist_ok=True)
        return dir


    def do_search(self, translator: "CPNTranslator", test_case: "TestCase") -> str:
        translator_working_directory = translator.get_translation_directory(test_case)

        param_str = "" if len(self.parameters)==0 else f'''"{'" "'.join(self.parameters)}"'''

        return f"""\
java \
{os.path.relpath(self.engine_path, translator_working_directory)} \
{param_str} \
"""
    #TODO: Fix when submodule installed

    def get_result_path(self, translator: "BaseTranslator", test_case: "TestCase", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_{iterator}.txt")

    def get_result_time_path(self, translator: "BaseTranslator", test_case: "TestCase", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_time_{iterator}.txt")
    
    def generate_search_script_content(self, translator: BaseTranslator, test_case: TestCase) -> str:
        return self._generate_search_script_content_base(translator, test_case) + f"""\
time {self.do_search(translator, test_case)}
"""