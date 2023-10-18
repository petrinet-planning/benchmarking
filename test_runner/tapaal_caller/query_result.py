import re
from re import Pattern

from ..planner_result import PlannerResult

from ..time_measurement import TimeMeasurement

regexes: dict[str, tuple[Pattern, type]] = {
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


class QueryResult(PlannerResult):
    
    @staticmethod
    def parse(query_output: str, print_unfound_keys: bool = False) -> "QueryResult":
        self = QueryResult()

        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(query_output)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self.output[name] = expected_type(found_value[1])

        return self

    def __repr__(self) -> str:
        return f"QueryResult(time_total={self.time_total})"