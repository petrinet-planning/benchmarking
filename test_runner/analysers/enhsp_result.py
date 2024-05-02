import re

from .search_result import SearchResult
from .plan import Plan, PlanAction
from unified_planning.io import PDDLReader
from ..test_case import TestCase
from .validate_trace import validate_plan

# TODO: change to suit output
regexes: dict[str, tuple[re.Pattern, type]] = {
    "has_plan": (re.compile(r"^(Solution found\.)", re.MULTILINE), str),
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
        
        self.has_plan = self.get("has_plan", False)
        if self.has_plan:
            self.plan = parse_sas_plan(test_case.domain_path, test_case.name)
            

        return self