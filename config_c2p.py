import os.path
import re

from test_runner import TestCase_c2p
from test_runner.test_validity_c2p import CpnBenchmarkValidity
from test_runner.translators import *
from test_runner.analysers import TapaalColoredResult, TapaalResult, TapaalSimpleResult, ENHSPResult
import time


validQueryLogPath = "validQueries.log.ignored"

def generate_valid_test_cases(benchmarks_basedir: str) -> list[TestCase_c2p]:

    open(validQueryLogPath, 'w').close() # Reset file
    def printToConsoleAndFile(msg):
        with open(validQueryLogPath, 'a') as f:
            f.write(msg+"\n")
            print(msg)


    domain_names = os.listdir(benchmarks_basedir)
    # domain_names = ["SafeBus-COL-03"]
    # domain_names = ["SafeBus-COL-06"]
    # domain_names = ["GlobalResAllocation-COL-03"]


    test_cases = []

    for domain_name in domain_names:
        model_path = os.path.join(benchmarks_basedir, domain_name, "model.pnml")
        queries_path = os.path.join(benchmarks_basedir, domain_name, "ReachabilityCardinality.xml")

        printToConsoleAndFile("Verifying " + domain_name)

        validity: CpnBenchmarkValidity = CpnBenchmarkValidity(model_path, queries_path)

        if not validity.valid_domain:
            continue

        printToConsoleAndFile("Succesfully verified: " + domain_name)

        for query_id, query_name in validity.queries:
            printToConsoleAndFile(f"Valid Query:\t{domain_name}\t{query_id}\t{query_name}")
            test_cases.append(TestCase_c2p(
                f"{domain_name} - {query_name}",
                model_path,
                queries_path,
                query_id,
                query_name
            ))

    return test_cases


def load_valid_test_cases(benchmarks_basedir: str) -> list[TestCase_c2p]:

    with open(validQueryLogPath, "r") as logFile:
        logText = logFile.read()

    logParserRegex = re.compile(r"Valid Query:\t(?P<domain_name>[^\t]+)\t(?P<xmlId>[^\t]+)\t(?P<queryName>[^\t\r\n]+)")
    
    test_cases = []
    for domain_name, query_id, query_name in logParserRegex.findall(logText):
        model_path = os.path.join(benchmarks_basedir, domain_name, "model.pnml")
        queries_path = os.path.join(benchmarks_basedir, domain_name, "ReachabilityCardinality.xml")
        
        test_cases.append(TestCase_c2p(
            f"{domain_name} - {query_name}",
            model_path,
            queries_path,
            query_id,
            query_name
        ))

    return test_cases

# all_valid_tests = generate_valid_test_cases("/mnt/c/Users/hginn/Downloads/Petri net benchmarks/MCC/MCC2023-COL")


tests = all_valid_tests



enhsp_path = os.path.abspath("test_runner/systems/enhsp-20/enhsp-dist/enhsp.jar")  # Cluster
tapaal_gui_path = os.path.abspath("test_runner/systems/tapaal-gui/build/distributions/TAPAAL-4.0-SNAPSHOT/bin/TAPAAL")  # Cluster
verifypnPath = "/nfs/home/student.aau.dk/hginne19/verifypn64"  # Cluster

# tapaal_gui_path = os.path.abspath("./test_runner/systems/tapaal_gui/build/distributions/TAPAAL-4.0-SNAPSHOT/bin/TAPAAL")

translation_count = 1
sample_count = 3
cluster_partition = "naples"
base_dir = "./experiments_c2p"

translators: list[BaseTranslator] = [
    DoNothingTranslator(translation_count, [
        TapaalSearcher_QuerySpecific(verifypnPath, "Tapaal", sample_count, TapaalColoredResult, ["--search-strategy", "RPFS"])
    ]),
    CpnToPddlTranslator(tapaal_gui_path, translation_count, [
        ENHSPSearcher(enhsp_path, "CpnToEnhsp", sample_count, [])
    ])
]

for translator in translators:
    translator.cluster_partition = cluster_partition
    translator.base_dir = base_dir
    for searcher in translator.searchers:
        searcher.cluster_partition = cluster_partition
