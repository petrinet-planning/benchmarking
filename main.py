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

# engine_path = "C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe"  # Windows
engine_path = "/mnt/c/Users/Henrik/Downloads/tapaal-4.0.0-linux64/tapaal-4.0.0-linux64/bin/verifypn64"  # Linux
runners: list[BaseTestRunner] = [
    LiftedPlanningRunner(engine_path, "Default Parameters", 50, ["--k-bound", "50", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"]),
    GroundedPlanningRunner(engine_path, "Default Parameters", 5, ["--k-bound", "50", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"])
]


csv_path = 'out_fixed.csv'
csv_file = open(csv_path, 'w')
csv_file.write("")
csv_file.close()

for test_case in tests:
    csv_file = open(csv_path, 'a')
    csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
    
    experiments_done = False
    i = 0
    while not experiments_done:  # Loop until i exceeds all runner sample-sizes
        experiments_done = True
        for runner in runners:
            if runner.needed_sample_size < i:
                continue
            experiments_done = False

            test_id = "{}_{}_{:02}".format(runner.translation_name, test_case.name, i)
            print(test_id)

            result: QueryResult = runner.run(test_case)
            
            csv_writer.writerow([
                runner.translation_name, 
                test_case.name,
                i,
                result.output["time_verification"],
                result.output["stats_expanded_states"],
                result.output["stats_explored_states"],
                result.output["stats_discovered_states"]
            ])
        i += 1

    csv_file.close()
