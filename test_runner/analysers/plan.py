
class PlanAction(object):
    action_name: str
    parameters: dict[str, str]

    def __init__(self, action_name: str, parameters: dict[str, str] = dict()) -> None:
        self.action_name = action_name
        self.parameters = parameters

    def __repr__(self) -> str:
        arg_str = ", ".join([f"{arg}={val}" for (arg, val) in self.parameters.items()])
        return f"action: {self.action_name}({arg_str})"

class Plan(object):
    actions: list[PlanAction]

    def __init__(self, actions: list[PlanAction] = list()) -> None:
        self.actions = actions
