import re
from re import Pattern

regexes: dict[str, tuple[re, type]] = {
    # Parameters
    "parameters": re.compile(r"^Parameters:([^\n]+)", re.MULTILINE),

    # Color
    "rwstats_colored_pre": re.compile(r"^RWSTATS COLORED PRE:((?:\d+,)+)", re.MULTILINE),
    "color_places": re.compile(r"^Size of colored net: (\d+) places, \d+ transitions, and \d+ arcs", re.MULTILINE),
    "color_transitions": re.compile(r"^Size of colored net: \d+ places, (\d+) transitions, and \d+ arcs", re.MULTILINE),
    "color_arcs": re.compile(r"^Size of colored net: \d+ places, \d+ transitions, and (\d+) arcs", re.MULTILINE),
    "color_places_unfolded": re.compile(r"^Size of unfolded net: (\d+) places, \d+ transitions, and \d+ arcs", re.MULTILINE),
    "color_transitions_unfolded": re.compile(r"^Size of unfolded net: \d+ places, (\d+) transitions, and \d+ arcs", re.MULTILINE),
    "color_arcs_unfolded": re.compile(r"^Size of unfolded net: \d+ places, \d+ transitions, and (\d+) arcs", re.MULTILINE),

    # Stats
    "stats_discovered_states": re.compile(r"^\tdiscovered states:\s*(\d+)", re.MULTILINE),
    "stats_explored_states": re.compile(r"^\texplored states:\s*(\d+)", re.MULTILINE),
    "stats_expanded_states": re.compile(r"^\texpanded states:\s*(\d+)", re.MULTILINE),
    "stats_max_tokens": re.compile(r"^\tmax tokens:\s*(\d+)", re.MULTILINE),

    # Query Reduction
    "query_reduction_finished_after": re.compile(r"^Query reduction finished after (\d+\.\d+) seconds", re.MULTILINE),
    "query_size_before_reduction": re.compile(r"^Query size reduced from (\d+) to \d+ nodes \( \d+ percent reduction\)", re.MULTILINE),
    "query_size_after_reduction": re.compile(r"^Query size reduced from \d+ to (\d+) nodes \( \d+ percent reduction\)", re.MULTILINE),

    # Net Reduction
    "place_count_before_reduction": re.compile(r"^Size of net before structural reductions: (\d+) places, \d+ transitions", re.MULTILINE),
    "place_count_after_reduction": re.compile(r"^Size of net after structural reductions: (\d+) places, \d+ transitions", re.MULTILINE),
    "transition_count_before_reduction": re.compile(r"^Size of net before structural reductions: \d+ places, (\d+) transitions", re.MULTILINE),
    "transition_count_after_reduction": re.compile(r"^Size of net after structural reductions: \d+ places, (\d+) transitions", re.MULTILINE),

    # Time
    "time_color_structural_reduction": re.compile(r"^Colored structural reductions computed in (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_color_fixpoint": re.compile(r"^Color fixpoint computed in (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_partitioned": re.compile(r"^Partitioned in (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_unfolding": re.compile(r"^Unfolded in (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_structural_reduction": re.compile(r"^Structural reduction finished after (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_potency": re.compile(r"^Potency initialization finished after (\d+(?:\.\d+)?) seconds", re.MULTILINE),
    "time_verification": re.compile(r"^Spent (\d+(?:\.\d+)?) on verification", re.MULTILINE),
}


class QueryResult:
    output: dict[str, Pattern[str]]

    translation_time: float
    tapaal_time: float

    def __init__(self):
        self.output = dict()

    @staticmethod
    def parse(query_output: str, print_unfound_keys: bool = False) -> "QueryResult":
        self = QueryResult()

        for name, regex in regexes.items():
            found_value = regex.search(query_output)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self.output[name] = found_value[1]

        return self
