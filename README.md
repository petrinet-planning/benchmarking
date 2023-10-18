# benchmarking

## Cloning
```sh
git clone https://github.com/petrinet-planning/benchmarking.git
cd benchmarking
git submodule update --init --recursive
```

## Requirements

## Compiling
On Linux, or Windows with WSL, run
```sh
./build_all.sh
```

For any compilation errors, consult the repo of each individual submodule.

## How to use


### Examples for manually calling each planner from commandline

Downward suboptimal:
```sh
python3 ./test_runner/systems/downward/fast-downward.py "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/domain.pddl" "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/p01.pddl" --evaluator "hff=ff()" --search "lazy_greedy([hff], preferred=[hff])"
```
```sh
python3 ./test_runner/systems/downward/fast-downward.py --alias lama-first "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/domain.pddl" "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/p01.pddl"
```

Grounded Translation:
```sh
python3 ./test_runner/systems/grounded_translation/src/fast-downward.py --keep-sas-file --mole max "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/domain.pddl" "benchmarks/autoscale-benchmarks/21.11-optimal-strips/blocksworld/p01.pddl" --goal --optimal
```

Lifted Translation:
```sh

```

## Updating all dependencies
```sh
git submodule update --remote --recursive --merge
```
