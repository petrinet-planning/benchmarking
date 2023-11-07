import os.path

from ..test_case import TestCase
from ..run_process import timed_command_piped_to_file

from .tapaal_translator import TapaalTranslator


grounded_translation_path = os.path.abspath("./test_runner/systems/grounded_translation/src/fast-downward.py")
class GroundedTranslator(TapaalTranslator):
    def __init__(self, sample_count: int, searches: list["TapaalSearcher"] = []) -> None:
        super().__init__("grounded", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None) -> str:
        translation_directory = self.get_translation_directory(test_case)

        return f"""\
python3 \
{os.path.relpath(grounded_translation_path, translation_directory)} \
--keep-sas-file --mole max \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
--goal --optimal \
"""

        return timed_command_piped_to_file([
            "python3",
            os.path.relpath(grounded_translation_path, translation_directory),
            "--keep-sas-file",
            "--mole", "max",
            os.path.relpath(test_case.domain_path, translation_directory),
            os.path.relpath(test_case.problem_path, translation_directory),
            "--goal", 
            "--optimal"
            ],
            directory=translation_directory,
            outfile=self.get_result_path(test_case, iterator),
            outfile_time=self.get_result_time_path(test_case, iterator)
        )

    def generate_translator_script_content(self, test_case: TestCase) -> str:
        return self._generate_translator_script_content_prefix(test_case) + f"""\
time {self.do_translation(test_case)}
"""

    def get_petrinet_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "out.pnml"))


    def get_query_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "out.xml"))
