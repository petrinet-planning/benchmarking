import re

from .tapaal_result import TapaalResult
from .plan import Plan, PlanAction


transition_meta_data_finder_regex = re.compile(r"transitionVars\[[^]]+\] = \{[^\}]+\}", flags=re.MULTILINE)
transition_meta_data_parser_transition_name_regex = re.compile(r"transitionVars\[\"(?P<transitionName>\w+)\"\]")
transition_meta_data_parser_variables_regex = re.compile(r"\"(?P<varname>[\w-]+):(?P<typename>[\w-]+)\": \"(?P<varvalue>[\w-]+)\", ")

trace_finder_regex = re.compile(r"<trace>.*</trace>", re.S)
trace_to_transition_names_regex = re.compile(r"<transition id=\"([^\"]+)\"")
unfolded_transition_to_action_name_regex = re.compile(r"(.*)_\d+")



class _Plan_Generator(object):
    transition_vars: dict[str, dict[str, str]] = dict()


    def parse_tapaal_output(self, tapaal_output: str) -> Plan:
        transition_map_strings = transition_meta_data_finder_regex.findall(tapaal_output)

        self.transition_vars = dict([self.parse_meta_data_line(transition_map_str) for transition_map_str in transition_map_strings])

        trace = self.get_trace(tapaal_output)

        actions = [self.unfolded_transition_to_action(transition_name) for transition_name in trace]

        return Plan(actions)

    
    def parse_meta_data_line(self, transition_map_str: str) -> tuple[str, dict[str, str]]:
        transition_name = transition_meta_data_parser_transition_name_regex.match(transition_map_str)["transitionName"]
        vars = dict([(name, value) for (name, typename, value) in transition_meta_data_parser_variables_regex.findall(transition_map_str)])

        return transition_name, vars
    

    def get_trace(self, tapaal_output) -> list[str]:
        trace_str = trace_finder_regex.search(tapaal_output)[0]

        transition_names = trace_to_transition_names_regex.findall(trace_str)

        return transition_names


    def unfolded_transition_to_action(self, unfolded_transition_name: str) -> PlanAction:
        action_name = unfolded_transition_to_action_name_regex.match(unfolded_transition_name)[1]
        vars = self.transition_vars[unfolded_transition_name]

        return PlanAction(action_name, vars)


class TapaalColoredResult(TapaalResult):

    def parse_result(self, file_content: str, print_unfound_keys: bool = False) -> "TapaalResult":
        TapaalResult.parse_result(self, file_content, print_unfound_keys)

        plan_generator = _Plan_Generator()
        self.plan = plan_generator.parse_tapaal_output(file_content)

        return self
    