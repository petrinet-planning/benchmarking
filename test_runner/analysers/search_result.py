from .base_result import BaseResult


class SearchResult(BaseResult, dict):
    has_plan: bool
    pass
