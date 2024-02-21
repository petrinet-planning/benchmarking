import unittest
from test_runner.analysers.plan import Plan, PlanAction
from unified_planning.model import Problem
from test_runner.analysers.validate_trace import reorder_plan, validate_plan

class TestValidateTrace(unittest.TestCase):
    def test_reorder_plan(self):
        cpn_plan = Plan([PlanAction("make_sandwich_no_gluten", {"s": "value1", "c": "value3", "b": "value2"})])
        pddl_domain_path = "benchmarks/autoscale-benchmarks/21.11-agile-strips/childsnack/domain.pddl"

        expected_ordered_actions = [PlanAction("make_sandwich_no_gluten", {"s": "value1", "b": "value2", "c": "value3"})]

        result = reorder_plan(cpn_plan, pddl_domain_path)

        self.assertEqual(result.actions, expected_ordered_actions)
    
    def test_reorder_plan2(self):
        cpn_plan = Plan([PlanAction("make_sandwich_no_gluten", {"s": "value1", "c": "value3", "b": "value2"}), PlanAction("make_sandwich_no_gluten", {"s": "value1", "b": "value2", "c": "value3"})])
        pddl_domain_path = "benchmarks/autoscale-benchmarks/21.11-agile-strips/childsnack/domain.pddl"

        expected_ordered_actions = [PlanAction("make_sandwich_no_gluten", {"s": "value1", "b": "value2", "c": "value3"}), PlanAction("make_sandwich_no_gluten", {"s": "value1", "b": "value2", "c": "value3"})]

        result = reorder_plan(cpn_plan, pddl_domain_path)
        print(result.planify())

        self.assertEqual(result.actions, expected_ordered_actions)

    def test_validate_plan(self):
        cpn_plan = Plan([PlanAction("make_sandwich_no_gluten", {"s": "value1", "c": "value3", "b": "value2"}), PlanAction("make_sandwich_no_gluten", {"s": "value1", "b": "value2", "c": "value3"})])
        pddl_domain_path = "benchmarks/autoscale-benchmarks/21.11-agile-strips/childsnack/domain.pddl"
        pddl_problem_path = "benchmarks/autoscale-benchmarks/21.11-agile-strips/childsnack/p01.pddl"

        result, msg = validate_plan(cpn_plan, pddl_domain_path, pddl_problem_path, ordered=True)

        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()

