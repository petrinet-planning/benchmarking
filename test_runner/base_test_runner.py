from . import TestCase


class BaseTestRunner:
    name: str

    def __init__(self, name: str):
        self.name = name

    def run(self, test_case: TestCase) -> str:
        pass
