import os.path

from test_runner import TestCase
from test_runner.planner_result import PlannerResult

from .test_case import TestCase
from .base_tapaal_runner import BaseTapaalTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query


class LiftedPlanningRunner(BaseTapaalTestRunner):
    description: str
    base_parameters: list[str]

    def __init__(self, tapaal_engine_path: str, description: str, needed_sample_size: int, base_parameters: list[str] = []):
        super().__init__("colored", description, needed_sample_size, tapaal_engine_path, base_parameters)

    def do_translation(self, test_case: TestCase, iterator: int = None) -> None:
        translation_directory = self.get_path_for_test_case(test_case)
        petrinet_path = os.path.abspath(os.path.join(translation_directory, "petrinet.pnml"))
        petrinet_query_path = os.path.abspath(os.path.join(translation_directory, "query.pnml"))
    
        translate_problem(test_case.domain_path, test_case.problem_path, petrinet_path, petrinet_query_path)

    def do_planning(self, test_case: TestCase, iterator: int = None) -> PlannerResult:
        translation_directory = self.get_path_for_test_case(test_case)
        petrinet_path = os.path.abspath(os.path.join(translation_directory, "petrinet.pnml"))
        petrinet_query_path = os.path.abspath(os.path.join(translation_directory, "query.pnml"))
    
        query = Query(pnml_path=petrinet_path, query_path=petrinet_query_path, parameters=self.base_parameters)
        query_output = query.run(self.tapaal_engine, self.experiment_work_directory, iterator)
        return query_output