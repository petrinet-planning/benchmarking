#! /bin/bash

# Copy from server
# rsync -av --exclude='venv/' deismcc_proxy:project/benchmarking/experiments experiments_from_server

# Copy to server
rsync -av --exclude='venv/' experiments deismcc_proxy:project/benchmarking

ssh deismcc_proxy "(cd project/benchmarking/experiments; sbatch run.sh)"



