from ..test_case_c2p import TestCase_c2p

from . import *

class TapaalSearcher_QuerySpecific(TapaalSearcher):

    def do_search(self, translator: "TapaalTranslator", test_case: "TestCase_c2p") -> str:
        baseStr = super().do_search(translator, test_case)
        
        return f"{baseStr} --xml-queries {test_case.query_id - 1}"