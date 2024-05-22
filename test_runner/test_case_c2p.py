from .test_case import TestCase

class TestCase_c2p(TestCase):
    query_id: int
    query_name: str

    def __init__(self, name: str, domain_path: str, problem_path: str, query_id: int, query_name: str) -> None:
        super().__init__(name, domain_path, problem_path)
        self.query_id = query_id
        self.query_name = query_name

