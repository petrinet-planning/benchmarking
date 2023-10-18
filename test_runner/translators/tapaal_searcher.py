import os.path

from ..run_process import timed_command_piped_to_file
from ..analysers import TapaalResult

from .base_searcher import BaseSearcher

class TapaalSearcher(BaseSearcher):
    parameters: list[str]
    engine_path: str
    parser: TapaalResult = TapaalResult

    def __init__(self, engine_path: str, name: str, sample_count: int, parameters: list[str] = []) -> None:
        super().__init__(name, sample_count)
        self.engine_path = engine_path
        self.parameters = parameters
    
    def out_dir(self, translator: "TapaalTranslator", test_case: "TestCase"):
        dir = os.path.join(translator.get_translation_directory(test_case), self.name)
        os.makedirs(dir, exist_ok=True)
        return dir

    def do_search(self, translator: "TapaalTranslator", test_case: "TestCase", iterator: int = None) -> None:
        petrinet_path = translator.get_petrinet_path(test_case)
        query_path = translator.get_query_path(test_case)

        timed_command_piped_to_file(
            [self.engine_path] + self.parameters + [petrinet_path, query_path],
            directory=translator.get_translation_directory(test_case),
            outfile= self.get_result_path(translator, test_case, iterator),
            outfile_time= self.get_result_time_path(translator, test_case, iterator)
        )

    def get_result_path(self, translator: "BaseTranslator", test_case: "TestCase", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_{iterator}.txt")

    def get_result_time_path(self, translator: "BaseTranslator", test_case: "TestCase", iterator: int):
        result_dir = os.path.abspath(self.out_dir(translator, test_case))
        return os.path.join(result_dir, f"result_search_time_{iterator}.txt")

