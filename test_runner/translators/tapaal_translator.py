from .base_translator import BaseTranslator
from .tapaal_searcher import TapaalSearcher

class TapaalTranslator(BaseTranslator):
    searchers: list["TapaalSearcher"]


    def __init__(self, name: str, sample_count: int, searchers: list["TapaalSearcher"] = []) -> None:
        super().__init__(name, sample_count, searchers)
