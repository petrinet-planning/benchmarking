import os.path

from test_runner import TestCase
from test_runner.test_validity import get_validity_code
from test_runner.translators import *
from test_runner.analysers import TapaalColoredResult, TapaalResult, TapaalSimpleResult
import time


def generate_valid_test_cases(benchmarks_basedir: str) -> list[TestCase]:
    domain_names = os.listdir(benchmarks_basedir)

    # Flat domains
    # domain_names = ["blocksworld", "childsnack", "ged", "miconic", "pegsol", "rovers", "scanalyzer", "visitall"]

    domain_names = ["blocksworld", "depots", "logistics", "nomystery", "visitall"]

    # Flat domains after arc fix
    # domain_names = ["blocksworld", "childsnack", "ged", "miconic", "pegsol", "rovers", "scanalyzer", "visitall", "freecell", "grid", "gripper", "logistics"]

    # Hierarchical domains
    #domain_names = ["blocksworld", "childsnack", "depots", "driverlog", "freecell", "ged", "grid", "gripper", "hiking", "logistics", "miconic", "mprime", "nomystery", "pegsol", "rovers", "scanalyzer", "tpp", "visitall"]
    
    # All domains
    # domain_names = ["agricola", "airport", "blocksworld", "childsnack", "data-network", "depots", "driverlog", "elevators", "floortile",
    #                 "freecell", "ged", "grid", "gripper", "hiking", "logistics", "miconic", "mprime", "nomystery", "openstacks", 
    #                 "organic-split-synthesis", "parcprinter", "parking", "pathways", "pegsol", "pipesworld-notankage", "pipesworld-tankage", 
    #                 "rovers", "scanalyzer", "snake", "sokoban", "storage", "termes", "tetris", "thoughtful", "tidybot", "tpp", "visitall",
    #                 "woodworking", "zenotravel"]
    p_range = range(1, 31)

    domain_validities = []

    for domain_name in domain_names:
        #print(f"Checking {domain_name}...")
        start_time = time.time()
        
        if os.path.isfile(os.path.join(benchmarks_basedir, domain_name, "domain.pddl")):
            validity = get_validity_code(f"{benchmarks_basedir}/{domain_name}/domain.pddl", f"{benchmarks_basedir}/{domain_name}/p01.pddl")
        else:
            validity = get_validity_code(f"{benchmarks_basedir}/{domain_name}/domain-p01.pddl", f"{benchmarks_basedir}/{domain_name}/p01.pddl")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{validity:02} - {domain_name}, {elapsed_time:.2f} seconds")

        domain_validities.append((domain_name, validity))


    valid_domains = [domain_name for (domain_name, validity) in domain_validities if validity == 0]

    test_cases = [
        TestCase(
            f"{domain_name}_{pnum:02}",
            os.path.join(benchmarks_basedir, domain_name, "domain.pddl") if os.path.isfile(os.path.join(benchmarks_basedir, domain_name, "domain.pddl")) else os.path.join(benchmarks_basedir, domain_name, f"domain-p{pnum:02}.pddl"),
            os.path.join(benchmarks_basedir, domain_name, f"p{pnum:02}.pddl"),
        ) 
        for domain_name in valid_domains
        for pnum in p_range
    ]

    return test_cases


all_valid_tests = generate_valid_test_cases("./benchmarks/autoscale-benchmarks/21.11-agile-strips")


tests = all_valid_tests


engine_path = "/nfs/home/student.aau.dk/hginne19/verifypn64"  # Cluster
engine_path_1safe = "/nfs/home/student.aau.dk/hginne19/P9/benchmarking/test_runner/systems/verifypn/build/verifypn/bin/verifypn-linux64"  # Cluster
engine_path_1safe_fast = "/nfs/home/student.aau.dk/slasse19/verifypn/build/verifypn/bin/verifypn-linux64" # Cluster, newer version, none of our bindings
downward_path = "./test_runner/systems/downward/fast-downward.py"


translation_count = 1
sample_count = 3
fast_mode = True

## -p, --disable-partial-order          Disable partial order reduction (stubborn sets)
# 0 interval
# -r 3 2,3,4,6,8,11,12

if fast_mode:
    engine_path_1safe = engine_path_1safe_fast

safe_reductions_only = ["--disable-partial-order"] + ["-r", "3", "2,3,4,6,8,11,12"]
unlimited_intervals = ["--max-intervals", "0", "0"]
fast_or_trace = ["--trace"] if not fast_mode else []
color_result_type = TapaalColoredResult if not fast_mode else TapaalSimpleResult
grounded_result_type = TapaalResult if not fast_mode else TapaalSimpleResult

cluster_partition = "dhabi"

translators: list[BaseTranslator] = [
    LiftedTranslator(translation_count, [
       # TapaalColorSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--trace"]),
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only),
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions_unlimited_intervals", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only + unlimited_intervals)
       # TapaalColorSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
       # TapaalColorSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "RandomWalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    LiftedHierarchyTranslator(translation_count, [
        # TapaalColorSearcher(engine_path_1safe, "rpfs", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--trace"]),
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only),
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions_unlimited_intervals", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only + unlimited_intervals)
        # TapaalColorSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
        # TapaalColorSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "RandomWalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    LiftedHierarchyV2Translator(translation_count, [
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only),
        TapaalColorSearcher(engine_path_1safe, "rpfs_safe_reductions_unlimited_intervals", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace + safe_reductions_only + unlimited_intervals)
    ]),
    GroundedTranslator(translation_count, [
        TapaalSearcher(engine_path, "rpfs", sample_count, grounded_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"] + fast_or_trace),
        # TapaalSearcher(engine_path_1safe, "no_color_optimizations", sample_count, ["--search-strategy", "RPFS", "--xml-queries", "1", "--disable-partitioning", "-D", "0", "--trace"]),
        # TapaalSearcher(engine_path_1safe, "randomwalk_1000_0", sample_count, ["--search-strategy", "Randomwalk", "1000", "0", "--xml-queries", "1", "--trace"]),
    ]),
    DownwardTranslator(translation_count, [
        DownwardSearcher(downward_path, "lama_first", sample_count, ["--alias", "lama-first"])
    ])    
]

for translator in translators:
    translator.cluster_partition = cluster_partition
    for searcher in translator.searchers:
        searcher.cluster_partition = cluster_partition
