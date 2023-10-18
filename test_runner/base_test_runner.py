import os
import os.path

from . import TestCase
from .translation_result import TranslationResult
from .planner_result import PlannerResult


class BaseTestRunner:
    translation_name: str
    description: str
    needed_sample_size: int  # Some configurations use random heuristics and should have higher sample size than deterministic configurations
    experiment_work_directory: str

    def __init__(self, translation_name: str, description: str, needed_sample_size: int, experiment_work_directory: str = None):
        self.translation_name = translation_name
        self.description = description
        self.needed_sample_size = needed_sample_size
        self.experiment_work_directory = experiment_work_directory if experiment_work_directory is not None else f"./experiments/{translation_name}/{description}/"

        os.makedirs(os.path.dirname(self.experiment_work_directory), exist_ok=True)

    def run(self, test_case: TestCase) -> str:
        pass

    def do_translation(self, test_case: TestCase, iterator: int = None) -> TranslationResult:
        raise Exception("Not implemented for base class")

    def do_planning(self, test_case: TestCase, iterator: int = None) -> PlannerResult:
        raise Exception("Not implemented for base class")

    def get_path_for_test_case(self, test_case: TestCase):
        path = os.path.join(self.experiment_work_directory, test_case.name)
        os.makedirs(path, exist_ok=True)
        return path

    def __repr__(self) -> str:
        return f"{self.translation_name}({self.description})"