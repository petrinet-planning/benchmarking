import os
import subprocess


def get_validity_code(domain_path: str, problem_path: str) -> int:
    domain_path_abs = os.path.abspath(domain_path)
    problem_path_abs = os.path.abspath(problem_path)

    validity_process = subprocess.run(["python3", "test_runner/systems/colored_translation_hierarchy/main.py", "--testValidity", domain_path_abs, problem_path_abs, "_", "_"])

    validity_code = validity_process.returncode

    return validity_code