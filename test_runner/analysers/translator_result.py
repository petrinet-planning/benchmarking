from .base_result import BaseResult
import re

class TranslatorResult(BaseResult):
    search_results: dict["BaseSearcher", list["SearchResult"]]
    valid_translation: bool

    def parse_result(self, file_content: str, test_case: "TestCase", print_unfound_keys: bool = False) -> None:
        super().parse_result(file_content, test_case, print_unfound_keys)
        self.valid_translation = not bool(re.search(r"exception", file_content, re.IGNORECASE))
    