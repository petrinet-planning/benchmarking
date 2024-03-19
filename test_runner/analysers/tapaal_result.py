import re

from .search_result import SearchResult
from .plan import Plan

regexes: dict[str, tuple[re.Pattern, type]] = {
    # Parameters
    "parameters": (re.compile(r"^Parameters:([^\n]+)", re.MULTILINE), str),

    # Color
    "rwstats_colored_pre": (re.compile(r"^RWSTATS COLORED PRE:((?:\d+,)+)", re.MULTILINE), str),
    "color_places": (re.compile(r"^Size of colored net: (\d+) places, \d+ transitions, and \d+ arcs", re.MULTILINE), int),
    "color_transitions": (re.compile(r"^Size of colored net: \d+ places, (\d+) transitions, and \d+ arcs", re.MULTILINE), int),
    "color_arcs": (re.compile(r"^Size of colored net: \d+ places, \d+ transitions, and (\d+) arcs", re.MULTILINE), int),
    "color_places_unfolded": (re.compile(r"^Size of unfolded net: (\d+) places, \d+ transitions, and \d+ arcs", re.MULTILINE), int),
    "color_transitions_unfolded": (re.compile(r"^Size of unfolded net: \d+ places, (\d+) transitions, and \d+ arcs", re.MULTILINE), int),
    "color_arcs_unfolded": (re.compile(r"^Size of unfolded net: \d+ places, \d+ transitions, and (\d+) arcs", re.MULTILINE), int),

    # Stats
    "stats_discovered_states": (re.compile(r"^\tdiscovered states:\s*(\d+)", re.MULTILINE), int),
    "stats_explored_states": (re.compile(r"^\texplored states:\s*(\d+)", re.MULTILINE), int),
    "stats_expanded_states": (re.compile(r"^\texpanded states:\s*(\d+)", re.MULTILINE), int),
    "stats_max_tokens": (re.compile(r"^\tmax tokens:\s*(\d+)", re.MULTILINE), int),

    # Query Reduction
    "query_size_before_reduction": (re.compile(r"^Query size reduced from (\d+) to \d+ nodes \( \d+ percent reduction\)", re.MULTILINE), int),
    "query_size_after_reduction": (re.compile(r"^Query size reduced from \d+ to (\d+) nodes \( \d+ percent reduction\)", re.MULTILINE), int),

    # Net Reduction
    "place_count_before_reduction": (re.compile(r"^Size of net before structural reductions: (\d+) places, \d+ transitions", re.MULTILINE), int),
    "place_count_after_reduction": (re.compile(r"^Size of net after structural reductions: (\d+) places, \d+ transitions", re.MULTILINE), int),
    "transition_count_before_reduction": (re.compile(r"^Size of net before structural reductions: \d+ places, (\d+) transitions", re.MULTILINE), int),
    "transition_count_after_reduction": (re.compile(r"^Size of net after structural reductions: \d+ places, (\d+) transitions", re.MULTILINE), int),

    # Time
    "time_query_reduction": (re.compile(r"^Query reduction finished after (\d+\.\d+) seconds", re.MULTILINE), float),
    "time_color_structural_reduction": (re.compile(r"^Colored structural reductions computed in (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_color_fixpoint": (re.compile(r"^Color fixpoint computed in (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_partitioned": (re.compile(r"^Partitioned in (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_unfolding": (re.compile(r"^Unfolded in (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_structural_reduction": (re.compile(r"^Structural reduction finished after (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_potency": (re.compile(r"^Potency initialization finished after (\d+(?:\.\d+)?) seconds", re.MULTILINE), float),
    "time_verification": (re.compile(r"^Spent (\d+(?:\.\d+)?) on verification", re.MULTILINE), float),
}


# Trace found?
trace_keywords_found_regex = re.compile(r"^Query is satisfied.\r?\nTrace:\r?\n<trace>", re.MULTILINE)

# Concrete structural reductions applied:
rule_application_regex = re.compile(r"^Applications of rule (\w+): (\d+)", re.MULTILINE)

class TapaalResult(SearchResult):
    plan: Plan

    # Parameters
    parameters: str

    # Color
    rwstats_colored_pre: str
    color_places: int
    color_transitions: int
    color_arcs: int
    color_places_unfolded: int
    color_transitions_unfolded: int
    color_arcs_unfolded: int
    
    # Stats
    stats_discovered_states: int
    stats_explored_states: int
    stats_expanded_states: int
    stats_max_tokens: int

    # Query Reduction
    query_size_before_reduction: int
    query_size_after_reduction: int

    # Net Reduction
    place_count_before_reduction: int
    place_count_after_reduction: int
    transition_count_before_reduction: int
    transition_count_after_reduction: int

    reductions_applied: dict[str, int]

    # Trace found?
    trace_keywords_found: str

    # Time
    time_query_reduction: float
    time_color_structural_reduction: float
    time_color_fixpoint: float
    time_partitioned: float
    time_unfolding: float
    time_structural_reduction: float
    time_potency: float
    time_verification: float

    def parse_result(self, file_content: str, print_unfound_keys: bool = False) -> "TapaalResult":
        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(file_content)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self[name] = expected_type(found_value[1])

        self.reductions_applied = dict()
        for reduction in rule_application_regex.findall(file_content):
            self.reductions_applied[reduction[0]] = int(reduction[1]) # First template = ruleID, second template = number of applications
        

        self["has_plan"] = trace_keywords_found_regex.match(file_content) != None

        return self
