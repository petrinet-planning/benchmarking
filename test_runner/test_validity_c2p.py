import os
import subprocess
import re


class CpnBenchmarkValidity:

    valid_domain: bool
    queries: list[tuple[int, str]]


    # static
    def __init__(self, domain_path: str, problem_path: str):
        domain_path_abs = os.path.abspath(domain_path)
        problem_path_abs = os.path.abspath(problem_path)
        
        regex = re.compile(r"Can parse pnml: (?P<modelSuccess>true|false)\r?\nValid queries:\r?\n(?P<queries>.*)$", 
            re.MULTILINE |
            re.DOTALL
        )
        queryLineRegex = re.compile(r"(?P<xmlId>\d+),(?P<queryName>[^\r\n]+)");

        validity_process = subprocess.run(["test_runner/systems/tapaal-gui/build/distributions/TAPAAL-4.0-SNAPSHOT/bin/TAPAAL", "-pddl-test", domain_path_abs, problem_path_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        matched = regex.search(validity_process.stdout.decode("utf-8"))
        if matched == None:
            self.valid_domain = False
            return
        
        matchdict = matched.groupdict()
        self.valid_domain = bool(matchdict["modelSuccess"])
        self.queries = [(int(xmlId), name) for (xmlId, name) in queryLineRegex.findall(matchdict["queries"])]