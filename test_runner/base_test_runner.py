from . import TestCase


class BaseTestRunner:
    translation_name: str
    description: str

    def __init__(self, translation_name: str, description: str):
        self.translation_name = translation_name
        self.description = description

    def run(self, test_case: TestCase) -> str:
        pass
