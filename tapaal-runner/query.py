import subprocess
from asyncio import Future
from typing import Optional, IO

from search_strategies import SearchStrategies
from engine import Engine
from query_result import QueryResult


class Query:
    pnml_path: str
    query_path: str
    k_bound: int
    search_strategy: SearchStrategies
    reductions_enabled: bool
    reductions_colored_enabled: bool
    path_to_write_reduced: Optional[str]

    def __init__(self,
                 pnml_path: str,
                 query_path: str,
                 k_bound: int,
                 search_strategy: SearchStrategies = SearchStrategies.random_heuristic,
                 reductions_enabled: bool = True,
                 reductions_colored_enabled: bool = True,
                 path_to_write_reduced: str = None
                 ):
        self.pnml_path = pnml_path
        self.query_path = query_path
        self.k_bound = k_bound
        self.search_strategy = search_strategy
        self.reductions_enabled = reductions_enabled
        self.reductions_colored_enabled = reductions_colored_enabled
        self.path_to_write_reduced = path_to_write_reduced

    def run(self, engine: Engine) -> str:
        p = subprocess.Popen([
            engine.verifypn_path,
            f"--k-bound", f"{self.k_bound}",
            "--search-strategy", self.search_strategy.value,
            f"--reduction", f"{'1' if self.reductions_enabled else '0'}",
            #("--write-reduced " + self.path_to_write_reduced) if self.path_to_write_reduced is not None else "",
            "--ctl-algorithm", "czero",
            "--xml-queries", "1",
            f"--col-reduction", f"{'1' if self.reductions_colored_enabled else '0'}",
            self.pnml_path,
            self.query_path
        ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        # Collect output
        output_lines = p.stdout.readlines()
        output_full = "".join([line.decode("utf-8") for line in output_lines])

        return output_full

