from . import TestCase


class BaseTestRunner:
    translation_name: str
    description: str
    needed_sample_size: int  # Some configurations use random heuristics and should have higher sample size than deterministic configurations

    def __init__(self, translation_name: str, description: str, needed_sample_size: int):
        self.translation_name = translation_name
        self.description = description
        self.needed_sample_size = needed_sample_size

    def run(self, test_case: TestCase) -> str:
        pass
