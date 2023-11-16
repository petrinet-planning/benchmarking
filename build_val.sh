#! /bin/bash
# sudo apt install bison cmake flex g++ git make python3 python3-venv
cd ./submodules/VAL
make clean  # Remove old binaries.
sed -i 's/-Werror //g' Makefile  # Ignore warnings.
make
cd ../..