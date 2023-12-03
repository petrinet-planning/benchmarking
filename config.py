import os.path

from test_runner import TestCase
from test_runner.test_validity import get_validity_code
from test_runner.translators import *



def generate_valid_test_cases(benchmarks_basedir: str) -> list[TestCase]:
    domain_names = os.listdir(benchmarks_basedir)
    domain_names = ["ged"]
    p_range = range(1, 4)

    domain_validities = [(domain_name, get_validity_code(f"{benchmarks_basedir}/{domain_name}/domain.pddl", f"{benchmarks_basedir}/{domain_name}/p01.pddl")) for domain_name in domain_names]
    
    for domain, validity in domain_validities:
        print(f"{validity:02} - {domain}")


    valid_domains = [domain_name for (domain_name, validity) in domain_validities if validity == 0]

    test_cases = [
        TestCase(
            f"{domain_name}_{pnum:02}",
            f"{benchmarks_basedir}/{domain_name}/domain.pddl",
            f"{benchmarks_basedir}/{domain_name}/p{pnum:02}.pddl",
        ) 
        for domain_name in valid_domains
        for pnum in p_range
    ]

    #valid_test_case = [case for case in all_test_cases if test_if_case_is_valid(case.domain_path, case.problem_path)]



    return test_cases


all_valid_tests = generate_valid_test_cases("./benchmarks/autoscale-benchmarks/21.11-agile-strips")

blocksworld_path = os.path.abspath("./benchmarks/autoscale-benchmarks/21.11-agile-strips/blocksworld")
blocksworld_domain_path = os.path.join(blocksworld_path, "domain.pddl")

blocksworld: list[TestCase] = [
    TestCase("blocksworld_01", blocksworld_domain_path, os.path.join(blocksworld_path, "p01.pddl")),
    TestCase("blocksworld_02", blocksworld_domain_path, os.path.join(blocksworld_path, "p02.pddl")),
    TestCase("blocksworld_03", blocksworld_domain_path, os.path.join(blocksworld_path, "p03.pddl")),
    TestCase("blocksworld_04", blocksworld_domain_path, os.path.join(blocksworld_path, "p04.pddl")),
    TestCase("blocksworld_05", blocksworld_domain_path, os.path.join(blocksworld_path, "p05.pddl")),
    TestCase("blocksworld_06", blocksworld_domain_path, os.path.join(blocksworld_path, "p06.pddl")),
    TestCase("blocksworld_07", blocksworld_domain_path, os.path.join(blocksworld_path, "p07.pddl")),
    TestCase("blocksworld_08", blocksworld_domain_path, os.path.join(blocksworld_path, "p08.pddl")),
    TestCase("blocksworld_09", blocksworld_domain_path, os.path.join(blocksworld_path, "p09.pddl")),
    TestCase("blocksworld_10", blocksworld_domain_path, os.path.join(blocksworld_path, "p10.pddl")),
    TestCase("blocksworld_11", blocksworld_domain_path, os.path.join(blocksworld_path, "p11.pddl")),
    TestCase("blocksworld_12", blocksworld_domain_path, os.path.join(blocksworld_path, "p12.pddl"))
]


snake_path = os.path.abspath("./benchmarks/autoscale-benchmarks/21.11-agile-strips/snake")
snake_domain_path = os.path.join(blocksworld_path, "domain.pddl")

snake: list[TestCase] = [
    TestCase("snake_01", snake_domain_path, os.path.join(snake_path, "p01.pddl")),
    # TestCase("snake_02", snake_domain_path, os.path.join(snake_path, "p02.pddl")),
    # TestCase("snake_03", snake_domain_path, os.path.join(snake_path, "p03.pddl")),
    # TestCase("snake_04", snake_domain_path, os.path.join(snake_path, "p04.pddl")),
    # TestCase("snake_05", snake_domain_path, os.path.join(snake_path, "p05.pddl")),
    # TestCase("snake_06", snake_domain_path, os.path.join(snake_path, "p06.pddl")),
    # TestCase("snake_07", snake_domain_path, os.path.join(snake_path, "p07.pddl")),
    # TestCase("snake_08", snake_domain_path, os.path.join(snake_path, "p08.pddl")),
    # TestCase("snake_09", snake_domain_path, os.path.join(snake_path, "p09.pddl")),
    # TestCase("snake_10", snake_domain_path, os.path.join(snake_path, "p10.pddl")),
    # TestCase("snake_11", snake_domain_path, os.path.join(snake_path, "p11.pddl")),
    # TestCase("snake_12", snake_domain_path, os.path.join(snake_path, "p12.pddl"))
]

tests = all_valid_tests


engine_path = "/nfs/home/student.aau.dk/hginne19/verifypn64"  # Cluster
engine_path_1safe = "/nfs/home/student.aau.dk/hginne19/verifypn1safe"  # Cluster

downward_path = "./test_runner/systems/downward/fast-downward.py"

translation_count = 1
sample_count = 2

translators: list[BaseTranslator] = [
    LiftedTranslator(translation_count, [
        TapaalSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1"]),
        TapaalSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0"]),
        TapaalSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "Randomwalk", "1000", "0", "--xml-queries", "1"]),
    ]),
    GroundedTranslator(translation_count, [
        TapaalSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1"]),
        TapaalSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0"]),
        TapaalSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "Randomwalk", "1000", "0", "--xml-queries", "1"]),
    ]),
    DownwardTranslator(translation_count, [
        DownwardSearcher(downward_path, "lama_first", sample_count, ["--alias", "lama-first"])
    ])    
]