
class PlanAction(object):
    action_name: str
    parameters: dict[str, str]

    def __init__(self, action_name: str, parameters: dict[str, str] = dict()) -> None:
        self.action_name = action_name
        self.parameters = parameters

    def __repr__(self) -> str:
        arg_str = ", ".join([f"{arg}={val}" for (arg, val) in self.parameters.items()])
        return f"action: {self.action_name}({arg_str})"
    
    #The dictionaries are turned into lists so that the order of the parameters has to be the same. This may not work in versions <3.7
    def __eq__(self, other):
        if isinstance(other, PlanAction):
            return self.action_name == other.action_name and list(self.parameters.items()) == list(other.parameters.items())
        return False

class Plan(object):
    actions: list[PlanAction]

    def __init__(self, actions: list[PlanAction] = list()) -> None:
        self.actions = actions

    def __repr__(self) -> str:
        return f"Plan({self.actions})"

    def planify(self):
        return '\n'.join([f"({action.action_name} {' '.join([f'{value}' for _, value in action.parameters.items()])})" for action in self.actions])
