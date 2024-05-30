from parse_results import parse

if __name__ == "__main__":
    from config_c2p import translators, tests

    parse(translators, tests)
    