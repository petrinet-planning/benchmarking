from asyncio import Future
from typing import IO
import re


regex_rwstats_colored_pre = re.compile(r"^RWSTATS COLORED PRE:((?:\d+,)+)", re.MULTILINE)

regex_removed_transitions = re.compile(r"^Removed transitions: (\d+)", re.MULTILINE)
regex_removed_places = re.compile(r"^Removed places: (\d+)", re.MULTILINE)

regex_stats_discovered_states = re.compile(r"^\tdiscovered states:\s*(\d+)", re.MULTILINE)
regex_stats_explored_states = re.compile(r"^\texplored states:\s*(\d+)", re.MULTILINE)
regex_stats_expanded_states = re.compile(r"^\texpanded states:\s*(\d+)", re.MULTILINE)
regex_stats_max_tokens = re.compile(r"^\tmax tokens:\s*(\d+)", re.MULTILINE)
regex_time_spent_on_verification = re.compile(r"^Spent (\d+.\d+) on verification", re.MULTILINE)


class QueryResult:
    rwstats_colored_pre: str

    removed_transitions: int
    removed_places: int

    stats_discovered_states: int
    stats_explored_states: int
    stats_expanded_states: int
    stats_max_tokens: int
    time_spent_on_verification: float

    def __init__(self):
        pass

    @staticmethod
    def parse(query_output: str) -> "QueryResult":
        self = QueryResult()

        # self.rwstats_colored_pre = regex_rwstats_colored_pre.search(query_output)[1]

        self.removed_transitions = int(regex_removed_transitions.search(query_output)[1])
        self.removed_places = int(regex_removed_places.search(query_output)[1])

        self.stats_discovered_states = int(regex_stats_discovered_states.search(query_output)[1])
        self.stats_explored_states = int(regex_stats_explored_states.search(query_output)[1])
        self.stats_expanded_states = int(regex_stats_expanded_states.search(query_output)[1])
        self.stats_max_tokens = int(regex_stats_max_tokens.search(query_output)[1])
        self.time_spent_on_verification = float(regex_time_spent_on_verification.search(query_output)[1])

        return self
