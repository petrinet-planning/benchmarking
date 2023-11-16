#! /bin/bash

echo "transforming trace to sas_plan"
bash python3 trace-to-plan.py "blocksworld_p01_grounded_trace.txt"

echo "validating plan"
bash validate ../benchmarks/autoscale-benchmarks/21.11-agile-strips/blocksworld/domain.pddl ../benchmarks/autoscale-benchmarks/21.11-agile-strips/blocksworld/p01.pddl tapaal_sas_plan