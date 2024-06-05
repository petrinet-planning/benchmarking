from .translator_result import TranslatorResult
import re



regexes: dict[str, tuple[re.Pattern, type]] = {
    "exprTooDeep_stringBuilder": (re.compile(r"(Exception in thread \"main\" java\.lang\.StackOverflowError\s+at\s+java\.base/java\.lang\.String\.valueOf\(String\.java:4461\)\s+at java\.base/java\.lang\.StringBuilder\.append\(StringBuilder\.java:173\))", re.MULTILINE), str),
    "exprTooDeep_rawExpr":       (re.compile(r"""(Exception in thread "main" java.lang.StackOverflowError\n\tat dk.aau.cs.pddl.expression.BaseExpression.toString\(BaseExpression.java:\d+\)\n\tat dk.aau.cs.pddl.expression.BaseExpression.toString\(BaseExpression.java:\d+\)\n\tat java.base/java.lang.String.valueOf\(String.java:\d+\)\n\tat java.base/java.lang.StringBuilder.append\(StringBuilder.java:\d+\)\n\tat dk.aau.cs.pddl.expression.BaseExpression.toString\(BaseExpression.java:\d+\)\n\tat dk.aau.cs.pddl.expression.BaseExpression.toString\(BaseExpression.java:\d+\))""", re.MULTILINE), str),
    "success": (re.compile(r"(Debug logging is enabled by default in DEV branch\s+real)", re.MULTILINE), str),
    "OutOfMemory": (re.compile(r"^(Exception in thread \"main\" java.lang.OutOfMemoryError: Java heap space)", re.MULTILINE), str),
    "StackOverflow": (re.compile(r"^(Exception in thread \"main\" java.lang.StackOverflowError)", re.MULTILINE), str),
    "NullPointerException": (re.compile(r"(java.lang.NullPointerException)", re.MULTILINE), str),
    "PnmlParserError": (re.compile(r"""(The color "[^"]+" was not declared\n\n\tat dk\.aau\.cs\.io\.LoadTACPN\.getColor\(LoadTACPN\.java:371\)\n\tat dk\.aau\.cs\.io\.LoadTACPN\.parseColorExpression\(LoadTACPN\.java:319\)\n\tat dk\.aau\.cs\.io\.LoadTACPN\.parseColorExpression\(LoadTACPN\.java:348\)\n\tat dk\.aau\.cs\.io\.LoadTACPN\.parseColorExpression\(LoadTACPN\.java:337\))""", re.MULTILINE), str),
}


class CpnToPddlTranslatorResult(TranslatorResult):
    search_results: dict["BaseSearcher", list["SearchResult"]]
    valid_translation: bool
    success: bool

    def parse_result(self, file_content: str, test_case: "TestCase", print_unfound_keys: bool = False) -> "CpnToPddlTranslatorResult":
        super().parse_result(file_content, test_case, print_unfound_keys)
        self.valid_translation = not bool(re.search(r"exception", file_content, re.IGNORECASE))

        for name, (regex, expected_type) in regexes.items():
            found_value = regex.search(file_content)
            if found_value is None:
                if print_unfound_keys:
                    print(f"No value found for {name}")
            else:
                self[name] = expected_type(found_value[1])

        self.success = self.get("success", False)

        return self