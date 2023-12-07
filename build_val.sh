#! /bin/bash
# sudo apt install bison cmake flex g++ git make python3 python3-venv
cd ./submodules/VAL
rm -r build
bash scripts/linux/build_linux64.sh all Release
