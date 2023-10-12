

from .test_case import TestCase
from .base_tapaal_runner import BaseTapaalTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query


class LiftedPlanningRunner(BaseTapaalTestRunner):
    description: str
    base_parameters: list[str]

    def __init__(self, tapaal_engine_path: str, description: str, base_parameters: list[str] = []):
        super().__init__("colored", description, tapaal_engine_path, base_parameters)

    def do_translation(self, test_case: TestCase) -> None:
        translate_problem(test_case.domain_path, test_case.problem_path, pnml_output_path="petrinet.pnml", pnml_query_path="query.xml")

    def do_tapaal(self) -> str:

        query = Query(pnml_path="petrinet.pnml", query_path="query.xml", parameters=self.base_parameters)
        query_output = query.run(self.tapaal_engine)
        return query_output