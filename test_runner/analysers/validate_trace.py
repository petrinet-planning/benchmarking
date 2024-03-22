from .plan import Plan, PlanAction
from unified_planning.io import PDDLReader
from unified_planning.model import Problem
from unified_planning.shortcuts import PlanValidator
import subprocess
import os
import re
    

def reorder_plan(cpn_plan: Plan, pddl_domain_path: str):
    ordered_actions: [PlanAction] = []
    reader = PDDLReader()
    domain = reader.parse_problem(pddl_domain_path)

    saved_actions: dict[str, list] = {action.name: action.parameters for action in domain.actions}
    for action in cpn_plan.actions:
        parameters: dict[str, str] = dict()
        for param in saved_actions[action.action_name]:
            parameters[param.name] = action.parameters.get(param.name)
        ordered_actions.append(PlanAction(action.action_name, parameters))

    # for action in cpn_plan.actions:
    #     for domain_action in domain.actions:
    #         if action.action_name == domain_action.name:
    #             parameters: dict[str, str] = dict()
    #             for param in domain_action.parameters:
    #                 parameters[param.name] = action.parameters.get(param.name) 
    #             ordered_actions.append(PlanAction(domain_action.name, parameters))

    return Plan(ordered_actions)


def validate_plan(cpn_plan: Plan, pddl_domain_path: str, pddl_problem_path: str, ordered: bool = False, filename: str = "sas_plan") -> (bool, str):
    plan = reorder_plan(cpn_plan, pddl_domain_path) if not ordered else cpn_plan
    
    with open(filename, 'w') as file:
        file.write(plan.planify())

    validate_path = f"{os.getcwd()}/submodules/VAL/build/linux64/Release/bin/Validate"

    process = subprocess.Popen([validate_path, pddl_domain_path, pddl_problem_path, filename], stdout=subprocess.PIPE)
    output, error = process.communicate()
    response = output.decode()

    return (True, "Plan valid") if re.search(r"Plan valid", response) is not None else (False, response)

    """
validate pddl_domain_path pddl_problem_path sas_plan

Checking plan: sas_plan
Plan executed successfully - checking goal
Plan valid
Final value: 28 

Successful plans:
Value: 28
 sas_plan 28 """
    return True
   
    


#reader = PDDLReader()
#domain = reader.parse_problem("benchmarks/autoscale-benchmarks/21.11-agile-strips/childsnack/domain.pddl")
#print("goimer")
