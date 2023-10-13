import subprocess

from test_runner.tapaal_caller.engine import Engine


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

    def run(self, engine: Engine) -> str:
        p = subprocess.run(
            [engine.verifypn_path] + self.parameters + [self.pnml_path, self.query_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )

        # Collect output
        output_full = p.stdout.decode("utf-8")

        return output_full

