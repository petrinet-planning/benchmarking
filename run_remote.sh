#! /bin/bash

# Copy from server
# rsync -av --exclude='colored_venv/' --exclude='venv/' deismcc_proxy:P9/benchmarking/experiments experiments_from_server
# rsync -av --exclude='colored_venv/' --exclude='venv/' deismcc_proxy:P9/benchmarking/experiments/colored/pegsol_01 experiments_from_server
# rsync -av --exclude='colored_venv/' --exclude='venv/' deismcc_proxy:P9/benchmarking/results .

# Copy to server
python3 generate_experiment_scripts.py 
rsync -av --exclude='venv/' experiments deismcc_proxy:P9/benchmarking
ssh deismcc_proxy "(cd P9/benchmarking/experiments; sbatch run.sh)"


ssh deismcc_proxy "(cd P9/benchmarking; srun python3 parse_results.py)"

# Update colored translation on server
# rsync -av --exclude='venv/' --exclude='__pycache__' test_runner/systems/colored_translation deismcc_proxy:project/benchmarking/test_runner/systems

# Update verifypn on server
# rsync -av --exclude='cmake-build-debug/' --exclude='.idea' test_runner/systems/verifypn deismcc_proxy:project/benchmarking/test_runner/systems


# Zip and download:
# ssh deismcc_proxy "(cd project/benchmarking; sbatch cleanup_and_zip_experiments.sh)"
# rsync -av deismcc_proxy:project/benchmarking/experiments.tar.gz experiments_from_server

# Download results
# rsync -av deismcc_proxy:P9/benchmarking/results .
# rsync -av deismcc_proxy:/nfs/home/student.aau.dk/hginne19/project/benchmarking/results .


