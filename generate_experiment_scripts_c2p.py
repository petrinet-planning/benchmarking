from generate_experiment_scripts import * 

def make_init_runner_file(translators: list[BaseTranslator], test_cases: list[TestCase]) -> str:
    newline = "\n"
    return f"""\
#!/bin/bash

{newline.join([f'(cd {translator.name}/{test.name}; sbatch run.sh)' for translator in translators for test in test_cases])}

"""

if __name__ == "__main__":
    from config_c2p import translators, tests

    generate_scripts(translators, tests, "./experiments_c2p")
