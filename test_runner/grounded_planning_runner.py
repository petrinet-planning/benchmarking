import re
import os.path

from test_runner import TestCase
from .run_process import run_process_timed, timed_command_piped_to_file

from . import TestCase
from .base_tapaal_runner import BaseTapaalTestRunner
from .tapaal_caller import Query


regex_find_place_value_in_query = re.compile("((?P<place>\w+) >= (?P<tokens>\d+))")
downward_path = os.path.abspath("./test_runner/systems/grounded_translation/src/fast-downward.py")

class GroundedPlanningRunner(BaseTapaalTestRunner):
    def __init__(self, tapaal_engine_path: str, description: str, needed_sample_size: int, base_parameters: list[str] = []):
        super().__init__("GnadGjoel", description, needed_sample_size, tapaal_engine_path, base_parameters)
    
    def do_translation(self, test_case: TestCase, iterator: int = None) -> None:
        translation_directory = self.get_path_for_test_case(test_case)

        timed_command_piped_to_file([
            "python3",
            downward_path,
            "--keep-sas-file",
            "--mole", "max",
            test_case.domain_path,
            test_case.problem_path,
            "--goal", 
            "--optimal"
            ],
            directory=translation_directory,
            outfile=f"result_translation_{iterator}.txt",
            outfile_time=f"result_translation_time_{iterator}.txt"
        )


    def do_planning(self, test_case: TestCase, iterator: int = None) -> str:
        translation_directory = self.get_path_for_test_case(test_case)
        query = Query(pnml_path="out.pnml", query_path="out.xml", parameters=self.base_parameters)
        return query.run(self.tapaal_engine, working_directory=translation_directory, iterator=iterator)
