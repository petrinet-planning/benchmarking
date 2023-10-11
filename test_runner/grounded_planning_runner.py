

from . import BaseTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query, QueryResult, Engine


class GroundedPlanningRunner(BaseTestRunner):
    tapaal_engine: Engine

    def __init__(self, engine_path: str):
        super().__init__("gradGjoel")
        self.tapaal_engine = Engine(engine_path)

    def run(self, test_case: TestCase) -> QueryResult:
        petri_net_path = "out.pnml"
        petri_net_query_path = "out.q"

        translate_problem(test_case.domain_path, test_case.problem_path, petri_net_path, petri_net_query_path)

        query = Query(pnml_path=petri_net_path, query_path=petri_net_query_path, k_bound=50)
        query_output = query.run(self.tapaal_engine)
        query_output_parsed = QueryResult.parse(query_output)

        return query_output_parsed
