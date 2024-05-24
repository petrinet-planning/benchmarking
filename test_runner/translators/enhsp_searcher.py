import os.path

from ..analysers import ENHSPResult
from ..test_case_c2p import TestCase_c2p

from . import *

class ENHSPSearcher(BaseSearcher):
    parameters: list[str]
    engine_path: str
    parser: ENHSPResult = ENHSPResult

    def __init__(self, engine_path: str, name: str, sample_count: int, parameters: list[str] = []) -> None:
        super().__init__(name, sample_count)
        self.engine_path = engine_path
        self.parameters = parameters
    
    
    def out_dir(self, translator: "CpnToPddlTranslator", test_case: "TestCase_c2p"):
        dir = os.path.join(translator.get_translation_directory(test_case), self.name)
        os.makedirs(dir, exist_ok=True)
        return dir


    def do_search(self, translator: "CpnToPddlTranslator", test_case: "TestCase_c2p") -> str:
        translator_working_directory = translator.get_translation_directory(test_case)

        param_str = "" if len(self.parameters)==0 else f'''"{'" "'.join(self.parameters)}"'''

        modelPath = translator.get_model_path(test_case)
        taskPath = translator.get_query_path(test_case)

        return f"""\
$JAVA_HOME/bin/java -jar \
{os.path.relpath(self.engine_path, translator_working_directory)} \
-o {os.path.relpath(modelPath, translator_working_directory)} \
-f {os.path.relpath(taskPath, translator_working_directory)} \
{param_str} \
"""
    def get_result_path(self, translator: "BaseTranslator", test_case: "TestCase_c2p", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_{iterator}.txt")

    def get_result_time_path(self, translator: "BaseTranslator", test_case: "TestCase_c2p", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_time_{iterator}.txt")
    
    def generate_search_script_content(self, translator: BaseTranslator, test_case: TestCase_c2p) -> str:
        return self._generate_search_script_content_base(translator, test_case) + f"""\
time {self.do_search(translator, test_case)}
"""
