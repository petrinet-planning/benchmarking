from ..analysers import TapaalColoredResult, TapaalSimpleResult
from .tapaal_searcher import TapaalSearcher

class TapaalColorSearcher(TapaalSearcher):
    parser: TapaalColoredResult