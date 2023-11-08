import re

from .search_result import SearchResult

regexes: dict[str, tuple[re.Pattern, type]] = {
    "has_plan": (re.compile(r"^(Solution found\.)", re.MULTILINE), str),
}

class DownwardSearchResult(SearchResult):
    def parse_result(self, file_content: str, print_unfound_keys: bool = False) -> "DownwardSearchResult":
        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(file_content)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self[name] = expected_type(found_value[1])

        return self
