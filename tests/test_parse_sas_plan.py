import unittest
from test_runner import parse_sas_plan
from test_runner.analysers.plan import Plan, PlanAction

class TestParseSasPlan(unittest.TestCase):
    def test_parse_sas_plan(self):
        # Define a path to a test domain file
        domain_path = '/home/seb/repos/newnew/benchmarking/benchmarks/test/truckD.pddl'

        # Call the function with the test domain file
        result = parse_sas_plan(domain_path)

        # Check that the result is a Plan object
        self.assertIsInstance(result, Plan)

        
        # This will depend on the contents of the sas_plan file in root directory
        expected_plan_actions = [
            PlanAction('load', {'p': 'p0', 't': 't0', 'l': 'l0'}),
            PlanAction('drive', {'t': 't0', 'l1': 'l0', 'l2': 'l1'}),
            PlanAction('unload', {'p': 'p0', 't': 't0', 'l': 'l1'}),
        ]
        self.assertEqual(result.actions, expected_plan_actions)

if __name__ == '__main__':
    unittest.main()