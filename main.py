import os
import os.path

from test_runner import TestCase
from test_runner.translators import *
from test_runner.analysers import *

from generate_experiment_scripts import generate_scripts
import parse_results

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
    TestCase("blocksworld_08", blocksworld_domain_path, os.path.join(blocksworld_path, "p08.pddl")),
    TestCase("blocksworld_09", blocksworld_domain_path, os.path.join(blocksworld_path, "p09.pddl")),
    TestCase("blocksworld_10", blocksworld_domain_path, os.path.join(blocksworld_path, "p10.pddl")),
    TestCase("blocksworld_11", blocksworld_domain_path, os.path.join(blocksworld_path, "p11.pddl"))
]

# engine_path = "C:/Users/Henrik/Downloads/tapaal-4.0.0-win64/tapaal-4.0.0-win64/bin/verifypn64.exe"  # Windows
engine_path = "/mnt/c/Users/Henrik/Downloads/tapaal-4.0.0-linux64/tapaal-4.0.0-linux64/bin/verifypn64"  # Linux
# engine_path = "/nfs/home/student.aau.dk/hginne19/verifypn64"  # Cluster

is_cluster = True
engine_path = "/nfs/home/student.aau.dk/hginne19/verifypn64" if is_cluster else engine_path
run_cmd = "run " if is_cluster else ""
batch_cmd = "batch " if is_cluster else "./"
next_cmd = "next " if is_cluster else ""


translators: list[BaseTranslator] = [
    LiftedTranslator(2, [
        TapaalSearcher(engine_path, "default_parameters", 50, ["--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning", "--trace"])
    ]),
    GroundedTranslator(2, [
        TapaalSearcher(engine_path, "default_parameters", 50, ["--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning", "--trace"])
    ]),
]

# generate_scripts(translators, tests)

parse_results.parse(translators, tests)