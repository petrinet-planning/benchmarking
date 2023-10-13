import re
import subprocess

from test_runner import TestCase

from . import TestCase
from .base_tapaal_runner import BaseTapaalTestRunner
from .tapaal_caller import Query


regex_find_place_value_in_query = re.compile("((?P<place>\w+) >= (?P<tokens>\d+))")

class GroundedPlanningRunner(BaseTapaalTestRunner):
    def __init__(self, tapaal_engine_path: str, description: str, needed_sample_size: int, base_parameters: list[str] = []):
        super().__init__("GnadGjoel", description, needed_sample_size, tapaal_engine_path, base_parameters)
    
    def do_translation(self, test_case: TestCase) -> None:
        p = subprocess.Popen([
            "python3",
            "./test_runner/systems/grounded_translation/src/fast-downward.py",
            "--keep-sas-file",
            "--mole", "max",
            test_case.domain_path,
            test_case.problem_path,
            "--goal", 
            "--optimal"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self.convert_query("out.q", "out.xml")

    def do_tapaal(self) -> str:
        query = Query(pnml_path="out.pnml", query_path="out.xml", parameters=self.base_parameters)
        return query.run(self.tapaal_engine)

    def convert_query(self, query_path_from: str, query_path_to: str):
        # EF Atom_on_b1__b4_ >= 1 && Atom_on_b2__b1_ >= 1 && Atom_on_b4__b5_ >= 1 && Atom_on_b5__b3_ >= 1

        with open(query_path_from, "r") as input_query_file:
            input_query = input_query_file.read()


        matches = regex_find_place_value_in_query.findall(input_query)
        newline = "            \n"

        xml = f"""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<property-set xmlns="http://tapaal.net/">
  <property>
    <id>Final Marking Reachable</id>
    <description>Final Marking Reachable</description>
    <formula>
      <exists-path>
        <finally>
          <conjunction>
            {newline.join([f"<integer-ge><tokens-count><place>{match[1]}</place></tokens-count><integer-constant>{match[2]}</integer-constant></integer-ge>" for match in matches])}
          </conjunction>
        </finally>
      </exists-path>
    </formula>
  </property>
</property-set>
"""

        with open(query_path_to, "w") as output_query_file:
            output_query_file.write(xml)
