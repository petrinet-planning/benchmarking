import re

from .search_result import SearchResult
from .plan import Plan, PlanAction
from unified_planning.io import PDDLReader

regexes: dict[str, tuple[re.Pattern, type]] = {
    # Parameters

    # Color

    # Stats

    # Query Reduction
    
    # Net Reduction


    # Time
    "time_verification": (re.compile(r"^Spent (\d+(?:\.\d+)?) on verification", re.MULTILINE), float),
}


# Trace found?
trace_keywords_found_regex = re.compile(r"Query is satisfied\.")

# Concrete structural reductions applied:

class TapaalSimpleResult(SearchResult):

    # Parameters

    # Color
    
    # Stats

    # Query Reduction

    # Net Reduction

    # Trace found?
    trace_keywords_found: str

    # Time
    time_verification: float

    def parse_result(self, file_content: str, test_case: "TestCase", print_unfound_keys: bool = False) -> "TapaalResult":
        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(file_content)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self[name] = expected_type(found_value[1])

        self.has_plan = trace_keywords_found_regex.search(file_content) != None

        return self
