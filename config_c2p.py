import os.path

from test_runner import TestCase
from test_runner.test_validity import get_validity_code
from test_runner.translators import *
from test_runner.analysers import TapaalColoredResult, TapaalResult, TapaalSimpleResult, ENHSPResult
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

    #TODO: Fix after finding CPN benchmarks
    test_cases = [
        TestCase(
            f"{domain_name}_{pnum:02}",
            os.path.join(benchmarks_basedir, domain_name, "domain.pddl") if os.path.isfile(os.path.join(benchmarks_basedir, domain_name, "domain.pddl")) else os.path.join(benchmarks_basedir, domain_name, f"domain-p{pnum:02}.pddl"),
            os.path.join(benchmarks_basedir, domain_name, f"p{pnum:02}.pddl"),
        ) 
        for domain_name in domain_names
        for pnum in p_range
    ]

    return test_cases


all_valid_tests = generate_valid_test_cases("./benchmarks/autoscale-benchmarks/21.11-agile-strips")


tests = all_valid_tests



enhsp_path = "/nfs/home/student.aau.dk/slasse19/P9/benchmarking/test_runner/systems/ENHSP-Public/enhsp-dist/enhsp.jar"  # Cluster


translation_count = 1
sample_count = 3

# TODO: Fix parameters
translators: list[BaseTranslator] = [
    CPNTranslator(translation_count, [
        ENHSPSearcher(enhsp_path, "rpfs_safe_reductions", sample_count, color_result_type, ["--search-strategy", "RPFS", "--xml-queries", "1"])
        
    ])
]