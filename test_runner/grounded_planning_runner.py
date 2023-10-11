import re
import subprocess

from . import BaseTestRunner, TestCase
from .systems.colored_translation.main import translate_problem

from .tapaal_caller import Query, QueryResult, Engine


regex_find_place_value_in_query = re.compile("((?P<place>\w+) >= (?P<tokens>\d+))")

class GroundedPlanningRunner(BaseTestRunner):
    tapaal_engine: Engine

    def __init__(self, engine_path: str):
        super().__init__("gnadGjoel")
        self.tapaal_engine = Engine(engine_path)

    def run(self, test_case: TestCase) -> QueryResult:

        p = subprocess.Popen([
            "./test_runner/systems/grounded_translation/src/fast-downward.py",
            "--keep-sas-file",
            "--mole", "max",
            test_case.domain_path,
            test_case.problem_path,
            "--goal", 
            "--optimal"
        ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        self.convert_query("out.q", "out.xml")

        query = Query(pnml_path="out.pnml", query_path="out.xml", k_bound=50)
        query_output = query.run(self.tapaal_engine)

        query_output_parsed = QueryResult.parse(query_output)

        return query_output_parsed

    def convert_query(self, query_path_from: str, query_path_to: str):
        # EF Atom_on_b1__b4_ >= 1 && Atom_on_b2__b1_ >= 1 && Atom_on_b4__b5_ >= 1 && Atom_on_b5__b3_ >= 1

        input_query_file = open(query_path_from, "r")
        input_query = input_query_file.read()
        input_query_file.close()

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

        output_query_file = open(query_path_to, "w")
        output_query_file.write(xml)
        output_query_file.close()


