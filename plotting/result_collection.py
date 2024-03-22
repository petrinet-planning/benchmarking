

# infinite = float("inf")
# results_dir = "./results"
# plot_save_dir = "./results/plots"
# os.makedirs(plot_save_dir, exist_ok=True)
# results_path = "./results"

# domain_sub_range = range(1, 31)

infinite = float("inf")

class result_collection:
    translator_results: list[list["TranslatorResult"]]
    search_results: list[list["SearchResult"]]

    def get_results(self) -> list[tuple[list["TranslatorResult"], list["SearchResult"]]]:
        return zip(self.translator_results, self.search_results)


    display_name: str
    style: str
    color: str


    def __init__(self, domain_sub_range):
        self.translator_results = [list() for _ in domain_sub_range]
        self.search_results = [list() for _ in domain_sub_range]


    def set(self, domain_sub_id: int, translator_results: list["TranslatorResult"], search_results: list["SearcherResult"]):
        self.translator_results[domain_sub_id] = translator_results
        self.search_results[domain_sub_id] = search_results


# Unknown translator
class result_container_domain_searcher:
    translators: dict[str, result_collection]


    def __init__(self):
        self.translators = dict()


    def set(self, translator_name: str, _result_collection: result_collection):
        self.translators[translator_name] = _result_collection


# Unknown domain
class result_container_translator_searcher:
    domains: dict[str, result_collection]


    def __init__(self):
        self.domains = dict()


    def set(self, domain_name: str, _result_collection: result_collection):
        self.domains[domain_name] = _result_collection


# Unknown searcher
class result_container_translator_domain:
    searchers: dict[str, result_collection]


    def __init__(self):
        self.searchers = dict()


    def set(self, searcher_name: str, _result_collection: result_collection):
        self.searchers[searcher_name] = _result_collection


# Unknown domain, searcher
class result_container_translator:
    domains: dict[str, result_container_translator_domain]
    searchers: dict[str, result_container_translator_searcher]

    def __init__(self):
        self.domains = dict()
        self.searchers = dict()


    def set(self, domain_name: str, searcher_name: str, _result_collection: result_collection):
        if domain_name not in self.domains:
            self.domains[domain_name] = result_container_translator_domain()

        if searcher_name not in self.searchers:
            self.searchers[searcher_name] = result_container_translator_searcher()
        

        self.domains[domain_name].set(searcher_name, _result_collection)
        self.searchers[searcher_name].set(domain_name, _result_collection)


# Unknown translator, searcher
class result_container_domain:
    translators: dict[str, result_container_translator_domain]
    searchers: dict[str, result_container_domain_searcher]


    def __init__(self):
        self.translators = dict()
        self.searchers = dict()


    def set(self, translator_name: str, searcher_name: str, _result_collection: result_collection):
        if translator_name not in self.translators:
            self.translators[translator_name] = result_container_translator_domain()

        if searcher_name not in self.searchers:
            self.searchers[searcher_name] = result_container_domain_searcher()
        

        self.translators[translator_name].set(searcher_name, _result_collection)
        self.searchers[searcher_name].set(translator_name, _result_collection)


# Unknown translator, domain
class result_container_searcher:
    translators: dict[str, result_container_translator_searcher]
    domains: dict[str, result_container_domain_searcher]


    def __init__(self):
        self.translators = dict()
        self.domains = dict()


    def set(self, translator_name: str, domain_name: str, _result_collection: result_collection):
        if translator_name not in self.translators:
            self.translators[translator_name] = result_container_translator_searcher()

        if domain_name not in self.domains:
            self.domains[domain_name] = result_container_domain_searcher()
        

        self.translators[translator_name].set(domain_name, _result_collection)
        self.domains[domain_name].set(translator_name, _result_collection)


class result_container:
    translators: dict[str, result_container_translator]
    domains: dict[str, result_container_domain]
    searchers: dict[str, result_container_searcher]


    def __init__(self):
        self.translators = dict()
        self.domains = dict()
        self.searchers = dict()


    def set(self, translator_name: str, domain_name: str, searcher_name: str, _result_collection: result_collection):
        if translator_name not in self.translators:
            self.translators[translator_name] = result_container_translator()

        if domain_name not in self.domains:
            self.domains[domain_name] = result_container_domain()

        if searcher_name not in self.searchers:
            self.searchers[searcher_name] = result_container_searcher()
        

        self.translators[translator_name].set(domain_name, searcher_name, _result_collection)
        self.domains[domain_name].set(translator_name, searcher_name, _result_collection)
        self.searchers[searcher_name].set(translator_name, domain_name, _result_collection)


# results = result_container()


# def load_translator_results() -> translator_result_type:
#     with open(os.path.join(results_path, f"translator_results.pickle"), "rb") as f:
#         return pickle.load(f)


# def load_search_results() -> search_result_type:
#     with open(os.path.join(results_path, f"search_results.pickle"), "rb") as f:
#         return pickle.load(f)



# _loaded_translator_results: translator_result_type = load_translator_results()
# _loaded_search_results: search_result_type = load_search_results()


# # Translator -> domain -> result[]
# translator_results_str_lookup: dict[str, dict[str, "BaseTranslator"]] = dict()


# # Translator Results
# for translator, domains in _loaded_translator_results.items():
#     translator_results_str_lookup[translator.name] = dict()
#     for domain, test_results in domains.items():
#         translator_results_str_lookup[translator.name][domain.name] = test_results


# # Search Results
# domain_regex = re.compile(r"^(?P<domain>.+?)_(?P<id>\d\d)$", re.MULTILINE)
# for translator, translator_results in _loaded_search_results.items():
#     for domain, test_results in translator_results.items():
#         for searcher, search_results in test_results.items():

#             domain_name = domain_regex.match(domain.name)["domain"]
#             domain_sub_id = int(domain_regex.match(domain.name)["id"])

#             if (
#                 translator.name in results.translators and
#                 domain_name     in results.translators[translator.name].domains and
#                 searcher.name   in results.translators[translator.name].domains[domain_name].searchers
#             ):
#                 results.translators[translator.name].domains[domain_name].searchers[searcher.name].set(domain_sub_id, translator_results, search_results)
            
#             else:

#                 _result_collection = result_collection()
#                 _result_collection.set(domain_sub_id, translator_results, search_results)

#                 # results.set(translator.name, domain.name, searcher.name, _result_collection)
#                 results.set(translator.name, domain_name, searcher.name, _result_collection)


