import os.path

from ..run_process import timed_command_piped_to_file

from .tapaal_translator import TapaalTranslator


grounded_translation_path = os.path.abspath("./test_runner/systems/grounded_translation/src/fast-downward.py")
class GroundedTranslator(TapaalTranslator):
    def __init__(self, sample_count: int, searches: list["TapaalSearcher"] = []) -> None:
        super().__init__("grounded", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None):
        translation_directory = self.get_translation_directory(test_case)

        timed_command_piped_to_file([
            "python3",
            grounded_translation_path,
            "--keep-sas-file",
            "--mole", "max",
            test_case.domain_path,
            test_case.problem_path,
            "--goal", 
            "--optimal"
            ],
            directory=translation_directory,
            outfile=self.get_result_path(test_case, iterator),
            outfile_time=self.get_result_time_path(test_case, iterator)
        )


    def get_petrinet_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "out.pnml"))


    def get_query_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "out.xml"))
