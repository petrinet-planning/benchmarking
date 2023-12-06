
from ..analysers import TapaalColoredResult
from .tapaal_searcher import TapaalSearcher

class TapaalColorSearcher(TapaalSearcher):
    parser: TapaalColoredResult = TapaalColoredResult