from enum import Enum
from .base_result import BaseResult

class QueryResultStatus(Enum):
    unset = None
    satisfied = 1
    unsolvable = 2
    error = 3
    unknown = 4
    timeout = 5

class SearchResult(BaseResult, dict):
    has_plan: bool
    result_status: QueryResultStatus
    pass
