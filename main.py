import os
import os.path
import pickle

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

# engine_path = "C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe"  # Windows
engine_path = "/mnt/c/Users/Henrik/Downloads/tapaal-4.0.0-linux64/tapaal-4.0.0-linux64/bin/verifypn64"  # Linux
runners: list[BaseTestRunner] = [
    LiftedPlanningRunner(engine_path, "Default Parameters", 10, ["--k-bound", "200", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"]),
    GroundedPlanningRunner(engine_path, "Default Parameters", 10, ["--k-bound", "200", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"])
]

results_path = "./results/"
os.makedirs(os.path.dirname(results_path), exist_ok=True)

for test_case in tests:
    results: dict[TestCase, dict[BaseTestRunner, list[QueryResult]]] = {}
    results[test_case] = dict()
    for runner in runners:
        results[test_case][runner] = list()
        for i in range(0, runner.needed_sample_size):
            print("{}_{}_{:02}".format(runner.translation_name, test_case.name, i))
            results[test_case][runner].append(runner.run(test_case))


    with open(os.path.join(results_path, f"{test_case.name}.pickle"), "wb") as f:
        pickle.dump(results, f)
