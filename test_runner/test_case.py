from typing import Optional


class TestCase:
    name: str
    domain_path: str
    problem_path: str

    def __init__(self, name: str, domain_path: str, problem_path: str) -> None:
        self.name = name
        self.domain_path = domain_path
        self.problem_path = problem_path

    def __repr__(self) -> str:
        return self.name