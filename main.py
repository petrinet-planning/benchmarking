import os.path
import csv

from test_runner import TestCase, BaseTestRunner, LiftedPlanningRunner, GroundedPlanningRunner
from test_runner.tapaal_caller import QueryResult

blocksworld_path = os.path.abspath("./benchmarks/autoscale-benchmarks/21.11-agile-strips/blocksworld")
blocksworld_domain_path = os.path.join(blocksworld_path, "domain.pddl")

tests: list[TestCase] = [
    TestCase("blocksworld_01", blocksworld_domain_path, os.path.join(blocksworld_path, "p01.pddl")),
    TestCase("blocksworld_02", blocksworld_domain_path, os.path.join(blocksworld_path, "p02.pddl")),
    TestCase("blocksworld_03", blocksworld_domain_path, os.path.join(blocksworld_path, "p03.pddl")),
    TestCase("blocksworld_04", blocksworld_domain_path, os.path.join(blocksworld_path, "p04.pddl")),
    TestCase("blocksworld_05", blocksworld_domain_path, os.path.join(blocksworld_path, "p05.pddl")),
    TestCase("blocksworld_06", blocksworld_domain_path, os.path.join(blocksworld_path, "p06.pddl")),
    TestCase("blocksworld_07", blocksworld_domain_path, os.path.join(blocksworld_path, "p07.pddl")),
    TestCase("blocksworld_08", blocksworld_domain_path, os.path.join(blocksworld_path, "p08.pddl"))
]

runners: list[BaseTestRunner] = [
    LiftedPlanningRunner("C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe"),
    GroundedPlanningRunner("C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe")
]

csv_writer = csv.writer(open ('out.csv', 'w'), delimiter=',', lineterminator='\n')

for test_case in tests:
    for i in range(1, 50):
        for runner in runners:
            test_id = "{}_{}_{:02}".format(runner.name, test_case.name, i)
            result_path = "./results/{}_{}_{:02}.log".format(runner.name, test_case.name, i)
            print(result_path)

            result: QueryResult = runner.run(test_case)
            # print(result)
            csv_writer.writerow([runner.name, test_case.name, i, result.time_spent_on_verification, result.stats_expanded_states, result.stats_explored_states, result.stats_discovered_states])

