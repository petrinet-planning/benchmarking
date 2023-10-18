from ..run_process import run_process_timed, timed_command_piped_to_file
from ..tapaal_caller.engine import Engine


class Query:
    pnml_path: str
    query_path: str
    parameters: list[str]

    def __init__(self,
                 pnml_path: str,
                 query_path: str,
                 parameters: list[str] = []
                 ):
        self.pnml_path = pnml_path
        self.query_path = query_path
        self.parameters = parameters

    def run(self, engine: Engine, working_directory: str, iterator: int = None) -> str:
        output_full = timed_command_piped_to_file(
            [engine.verifypn_path] + self.parameters + [self.pnml_path, self.query_path],
            directory=working_directory,
            outfile=f"result_search_{iterator}.txt",
            outfile_time=f"result_search_time_{iterator}.txt"
        )

        return output_full

