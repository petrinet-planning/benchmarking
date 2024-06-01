import re
from collections import Counter

from .search_result import QueryResultStatus, SearchResult
from .plan import Plan, PlanAction
from unified_planning.io import PDDLReader
from ..test_case import TestCase
from .validate_trace import validate_plan

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

planRegex = re.compile(r"Found Plan:\r?\n(.+?\r?\n)\r?\n", re.MULTILINE)
planLineRegex = re.compile(r"(?P<cost>\d+\.\d+): \((?P<action>[^ ]+) (?P<parameters>[^\)]+)\)")
planParamRegex = re.compile(r"(?P<param>[^ ]+)")


class ENHSPResult(SearchResult):
    plan: Plan
    validation_result: (bool, str)
    plan_warning: bool

    def parse_plan(self, file_content: str) -> Plan:

        plan_text = re.compile(r"Found Plan:\r?\n([\s\S]+?\r?\n)\r?\n").search(file_content)[1]
    
        plan_actions: list[PlanAction] = []

        for cost, action_name, params_txt in planLineRegex.findall(plan_text):
            params = planParamRegex.findall(params_txt)
            anyDuplicateParams = True if [x for x in Counter(params).values() if x > 1] else False
            if anyDuplicateParams:
                self.plan_warning = True

            plan_actions.append(PlanAction(action_name, dict(zip(range(0,len(params)), params))))

        return Plan(plan_actions)

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

        self.has_plan = True if self.get("has_plan", False) else False
        self.plan_warning = False
        if self.has_plan:
            self.plan = self.parse_plan(file_content)
            

        return self