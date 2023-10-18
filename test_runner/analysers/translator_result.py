from .base_result import BaseResult


class TranslatorResult(BaseResult):
    search_results: dict["BaseSearcher", list["SearchResult"]]
    