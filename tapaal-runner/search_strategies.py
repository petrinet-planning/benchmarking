from enum import Enum


class SearchStrategies(Enum):
    random_heuristic = "RPFS"
    depth_first = "DFS"
    breadth_first = "BFS"
    random = "RDFS"
