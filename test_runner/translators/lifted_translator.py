import os.path

from ..run_process import timed_command_piped_to_file
from ..test_case import TestCase

from .tapaal_translator import TapaalTranslator


colored_translation_path = os.path.abspath("./test_runner/systems/colored_translation/main.py")
class LiftedTranslator(TapaalTranslator):
    def __init__(self, sample_count: int, searches: list["TapaalSearcher"] = []) -> None:
        super().__init__("colored", sample_count, searches)


    def do_translation(self, test_case: "TestCase", iterator: int = None) -> str:

        translation_directory = self.get_translation_directory(test_case)
        petrinet_path = self.get_petrinet_path(test_case)
        petrinet_query_path = self.get_query_path(test_case)

        return f"""\
"python3" \
"{os.path.relpath(colored_translation_path, translation_directory)}" \
"{os.path.relpath(test_case.domain_path, translation_directory)}" \
"{os.path.relpath(test_case.problem_path, translation_directory)}" \
"{os.path.relpath(petrinet_path, translation_directory)}" \
"{os.path.relpath(petrinet_query_path, translation_directory)}" \
"""



        return timed_command_piped_to_file([
                "python3",
                os.path.relpath(colored_translation_path, translation_directory),
                os.path.relpath(test_case.domain_path, translation_directory),
                os.path.relpath(test_case.problem_path, translation_directory),
                os.path.relpath(petrinet_path, translation_directory),
                os.path.relpath(petrinet_query_path, translation_directory),
            ],
            directory=translation_directory,
            outfile=self.get_result_path(test_case, iterator),
            outfile_time=self.get_result_time_path(test_case, iterator)
        )

    def generate_translator_script_content(self, test_case: TestCase) -> str:

        return self._generate_translator_script_content_prefix(test_case) + f"""\
python3 -m venv venv
source venv/bin/activate

python3 -m pip install unified_planning

time {self.do_translation(test_case)}
"""

    def get_petrinet_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "petrinet.pnml"))


    def get_query_path(self, test_case: "TestCase"):
        return os.path.abspath(os.path.join(self.get_translation_directory(test_case), "query.pnml"))
    