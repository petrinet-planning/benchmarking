import re

from .search_result import QueryResultStatus, SearchResult
from .plan import Plan, PlanAction
from unified_planning.io import PDDLReader
from ..test_case import TestCase
from .validate_trace import validate_plan

# TODO: change to suit output
regexes: dict[str, tuple[re.Pattern, type]] = {

    # Reductions
    "|F|": (re.compile(r"^\|F\|: ?(\d+)", re.MULTILINE), int),
    "|X|": (re.compile(r"^\|X\|: ?(\d+)", re.MULTILINE), int),
    "|A|": (re.compile(r"^\|A\|: ?(\d+)", re.MULTILINE), int),
    "|P|": (re.compile(r"^\|P\|: ?(\d+)", re.MULTILINE), int),
    "|E|": (re.compile(r"^\|E\|: ?(\d+)", re.MULTILINE), int),


    "has_plan": (re.compile(r"^(Found Plan:)", re.MULTILINE), str),
    "Problem unsolvable": (re.compile(r"^(Problem unsolvable)", re.MULTILINE), str),
    "OutOfMemory": (re.compile(r"^(Exception in thread \"main\" java.lang.OutOfMemoryError: Java heap space)", re.MULTILINE), str),
    "StackOverflow": (re.compile(r"^(Exception in thread \"main\" java.lang.StackOverflowError)", re.MULTILINE), str),
    "SyntaxError": (re.compile(r"^(no viable alternative at input)", re.MULTILINE), str),
    "TranslationFailed": (re.compile(r"^(java.io.FileNotFoundException)", re.MULTILINE), str),


    "Plan-Length": (re.compile(r"^Plan-Length: ?(\d+)", re.MULTILINE), int),
    "Metric (Search)": (re.compile(r"^Metric (Search): ?(\d+)", re.MULTILINE), float),
    "Planning Time (msec)": (re.compile(r"^Planning Time (msec):  ?(\d+)", re.MULTILINE), int),
    "Heuristic Time (msec)": (re.compile(r"^Heuristic Time (msec):  ?(\d+)", re.MULTILINE), int),
    "Search Time (msec)": (re.compile(r"^Search Time (msec):  ?(\d+)", re.MULTILINE), int),
    "Expanded Nodes": (re.compile(r"^Expanded Nodes: ?(\d+)", re.MULTILINE), int),
    "States Evaluated": (re.compile(r"^States Evaluated: ?(\d+)", re.MULTILINE), int),
    "Number of Dead-Ends detected": (re.compile(r"^Number of Dead-Ends detected: ?(\d+)", re.MULTILINE), int),
    "Number of Duplicates detected": (re.compile(r"^Number of Duplicates detected: ?(\d+)", re.MULTILINE), int),
    
}

def parse_sas_plan(domain_path: str, case_name: str):
    folder_name = f"experiments/downward/{case_name}/sas_plan"
    with open(folder_name, "r") as file:
        lines = [re.sub(r"[()]", "", line).strip() for line in file.readlines() if not line.startswith(';')]
        reader = PDDLReader()
        domain = reader.parse_problem(domain_path)

        plan_actions = []
        saved_actions: dict[str, list] = {action.name: action.parameters for action in domain.actions}
        for line in lines:
            parameters: dict[str, str] = dict()
            action, param_vals = line.split()[0], line.split()[1:]

            i = 0
            for param in saved_actions[action]:
                parameters[param.name] = param_vals[i]
                i += 1
        
            plan_actions.append(PlanAction(action, parameters))

        return Plan(plan_actions)

class ENHSPResult(SearchResult):
    plan: Plan
    validation_result: (bool, str)

    def parse_result(self, file_content: str, test_case: TestCase, print_unfound_keys: bool = False) -> "ENHSPResult":
        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(file_content)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self[name] = expected_type(found_value[1])
        
        self.result_status = (
            QueryResultStatus.satisfied if self.get("has_plan", False) else
            QueryResultStatus.unsolvable if self.get("Problem unsolvable", False) else 
            QueryResultStatus.error if (
                self.get("OutOfMemory", False) or 
                self.get("StackOverflow", False) or 
                self.get("SyntaxError", False) or 
                self.get("TranslationFailed", False)
            ) else
            QueryResultStatus.unknown
        )

        self.has_plan = self.get("has_plan", False)
        # if self.has_plan:
        #     self.plan = parse_sas_plan(test_case.domain_path, test_case.name)
            

        return self