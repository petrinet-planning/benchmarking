

from . import BaseTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query, Engine


class LiftedPlanningRunner(BaseTestRunner):
    tapaal_engine: Engine

    def __init__(self, engine_path: str):
        super().__init__("colored")
        self.tapaal_engine = Engine(engine_path)

    def run(self, test_case: TestCase) -> str:
        petri_net_path = "petrinet.pnml"
        petri_net_query_path = "query.xml"

        translate_problem(test_case.domain_path, test_case.problem_path, petri_net_path, petri_net_query_path)

        query = Query(pnml_path=petri_net_path, query_path=petri_net_query_path, k_bound=50)
        query_output = query.run(self.tapaal_engine)

        return query_output
