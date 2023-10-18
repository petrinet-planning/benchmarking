import os.path

from ..run_process import timed_command_piped_to_file

from .tapaal_translator import TapaalTranslator


colored_translation_path = os.path.abspath("./test_runner/systems/colored_translation/main.py")
class LiftedTranslator(TapaalTranslator):
    def __init__(self, sample_count: int, searches: list["TapaalSearcher"] = []) -> None:
        super().__init__("colored", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None):
        translation_directory = self.get_translation_directory(test_case)
        petrinet_path = self.get_petrinet_path(test_case)
        petrinet_query_path = self.get_query_path(test_case)

        timed_command_piped_to_file([
            "python3",
            colored_translation_path,
            test_case.domain_path,
            test_case.problem_path,
            petrinet_path,
            petrinet_query_path
            ],
            directory=translation_directory,
            outfile=f"result_translation_{iterator}.txt",
            outfile_time=f"result_translation_time_{iterator}.txt"
        )


    def get_petrinet_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "petrinet.pnml"))


    def get_query_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "query.pnml"))
    
