import os.path

from test_runner import TestCase
from test_runner.test_validity import get_validity_code
from test_runner.translators import *


def generate_valid_test_cases(benchmarks_basedir: str) -> list[TestCase]:
    domain_names = os.listdir(benchmarks_basedir)

    # Flat domains
    # domain_names = ["blocksworld", "childsnack", "ged", "miconic", "pegsol", "rovers", "scanalyzer", "visitall"]

    # Flat domains after arc fix
    # domain_names = ["blocksworld", "childsnack", "ged", "miconic", "pegsol", "rovers", "scanalyzer", "visitall", "freecell", "grid", "gripper", "logistics"]

    # Hierarchical domains
    domain_names = ["blocksworld", "childsnack", "depots", "driverlog", "freecell", "ged", "grid", "gripper", "hiking", "logistics", "miconic", "mprime", "nomystery", "pegsol", "rovers", "scanalyzer", "tpp", "visitall"]
    p_range = range(1, 11)

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

    return test_cases


all_valid_tests = generate_valid_test_cases("./benchmarks/autoscale-benchmarks/21.11-agile-strips")


tests = all_valid_tests


engine_path = "/nfs/home/student.aau.dk/hginne19/verifypn64"  # Cluster
engine_path_1safe = "/nfs/home/student.aau.dk/hginne19/P9/benchmarking/test_runner/systems/verifypn/build/verifypn/bin/verifypn-linux64"  # Cluster
downward_path = "./test_runner/systems/downward/fast-downward.py"

translation_count = 1
sample_count = 2

translators: list[BaseTranslator] = [
    LiftedTranslator(translation_count, [
        TapaalColorSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--trace"]),
        # TapaalColorSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
        # TapaalColorSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "RandomWalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    LiftedHierarchyTranslator(translation_count, [
        TapaalColorSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--trace"]),
        # TapaalColorSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
        # TapaalColorSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "RandomWalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    GroundedTranslator(translation_count, [
        TapaalSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--trace"]),
        # TapaalSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
        # TapaalSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "Randomwalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    DownwardTranslator(translation_count, [
        DownwardSearcher(downward_path, "lama_first", sample_count, ["--alias", "lama-first"])
    ])    
]