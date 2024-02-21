import os
import os.path
import pickle

from test_runner import TestCase
from test_runner.translators import *
from test_runner.analysers import *

translator_result_type = dict[BaseTranslator, "TranslatorResult"]
search_result_type = dict[BaseTranslator, dict["TestCase", dict["BaseSearcher", list["SearchResult"]]]]

results_path = "./results"


def parse(translators: list[BaseTranslator], test_cases: list[TestCase]):
    translator_results: translator_result_type = dict()
    search_results: search_result_type = dict()

    for translator in translators:
        translator_results[translator] = translator.parse_results(test_cases)
        search_results[translator] = translator.parse_search_results(test_cases)

    return False
#    os.makedirs(results_path, exist_ok=True)
#    with open(os.path.join(results_path, f"translator_results.pickle"), "wb") as f:
#        pickle.dump(translator_results, f)
#
#    with open(os.path.join(results_path, f"search_results.pickle"), "wb") as f:
#        pickle.dump(search_results, f)


def load_translator_results() -> translator_result_type:
    with open(os.path.join(results_path, f"translator_results.pickle"), "rb") as f:
        return pickle.load(f)


def load_search_results() -> search_result_type:
    with open(os.path.join(results_path, f"search_results.pickle"), "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    from config import translators, tests

    parse(translators, tests)
    