import os

from test_runner import TestCase
from test_runner.translators import *
from test_runner.analysers import *

def make_init_runner_file(translators: list[BaseTranslator], test_cases: list[TestCase]) -> str:
    newline = "\n"
    return f"""\
#!/bin/bash

{newline.join([f'(cd {translator.name}/{test.name}; sbatch run.sh)' for translator in translators for test in test_cases])}

"""


def make_experiment_runner_file(translator: BaseTranslator, test_case: TestCase):
    newline = "\n"
    return f"""\
#!/bin/bash
#SBATCH -J "{translator.name} - {test_case.name}"
#SBATCH --partition=naples,dhabi

source /nfs/home/student.aau.dk/hginne19/slurm-dependencies.sh

run_many {translator.sample_count} --output "%A.translation.%a.txt" translate.sh

next

{newline.join([f'run_many {searcher.sample_count} --output "{searcher.name}/%A.search.%a.txt" "search_{searcher.name}.sh"' for searcher in translator.searchers])}

"""

def mkdir(str):
    os.makedirs(str, exist_ok=True)


def generate_scripts(translators: list[BaseTranslator], test_cases: list[TestCase]):

    mkdir("./experiments")
    with open("./experiments/run.sh", "w") as init_runner_file:
        init_runner_file.write(make_init_runner_file(translators, test_cases))

        for translator in translators:

            for test in test_cases:
                mkdir(f"./experiments/{translator.name}/{test.name}/")
                with open(f"./experiments/{translator.name}/{test.name}/translate.sh", "w") as experiment_translator_runner_file:
                    experiment_translator_runner_file.write(translator.generate_translator_script_content(test))

                with open(f"./experiments/{translator.name}/{test.name}/run.sh", "w") as experiment_runner_file:
                    experiment_runner_file.write(make_experiment_runner_file(translator, test))

                for searcher in translator.searchers:
                    mkdir(f"./experiments/{translator.name}/{test.name}/{searcher.name}")
                    searcher_file_name = f"./experiments/{translator.name}/{test.name}/search_{searcher.name}.sh"
                    with open(searcher_file_name, "w") as search_runner_file:
                        search_runner_file.write(searcher.generate_search_script_content(translator, test))

if __name__ == "__main__":
    from config import translators, tests

    generate_scripts(translators, tests)
