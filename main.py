import os
import os.path
import pickle

from test_runner import TestCase
from test_runner.translators import *
from test_runner.analysers import *

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

translators: list[BaseTranslator] = [
    LiftedTranslator(5, [
        TapaalSearcher(engine_path, "Default Parameters", 20, ["--k-bound", "200", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"])
    ]),
    GroundedTranslator(5, [
        TapaalSearcher(engine_path, "Default Parameters", 20, ["--k-bound", "200", "--search-strategy", "RPFS", "--reduction", "1", "--ctl-algorithm", "czero", "--xml-queries", "1", "--disable-partitioning"])
    ]),
    
]

open("run.sh", "w").close()
translator_results: dict[BaseTranslator, "TranslatorResult"] = dict()
search_results: dict[BaseTranslator, dict["TestCase", dict["BaseSearcher", list["SearchResult"]]]] = dict()

for translator in translators:
    translator_results[translator] = translator.parse_results(tests)
    search_results[translator] = translator.parse_search_results(tests)

results_path = "./results"
with open(os.path.join(results_path, f"translator_results.pickle"), "wb") as f:
    pickle.dump(translator_results, f)

with open(os.path.join(results_path, f"search_results.pickle"), "wb") as f:
    pickle.dump(search_results, f)

