#!/bin/bash #var=$((var + 1))
for f in ./PFSP_instances/*.txt; do
    python solvePFSP_MaxMin.py --instance $f
    #python writeData.py MaxMin $f $count
    #count=$((count + 1))
done