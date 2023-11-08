
def run_search_script(search_cmd: str) -> str:
    f"""\
#!/bin/bash
#SBATCH -J "colored - blocksworld_01 - search"
#SBATCH --mail-type=FAIL  # BEGIN,END,FAIL,ALL,NONE
#SBATCH --mail-user=hginne19@student.aau.dk
#SBATCH --partition=naples,dhabi
#SBATCH --time=1:00:00
#SBATCH --mem=16G

iterator=$1

let "m=1024*1024*1"
ulimit -v $m

time {search_cmd}
"""
