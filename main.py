from generate_experiment_scripts import generate_scripts
import parse_results

from config import translators, tests


generate_scripts(translators, tests)

# parse_results.parse(translators, tests)