#!/bin/bash
count=1
for f in ./PFSP_instances/*.txt; do
    python solvePFSP_ACS.py --instance $f
    python writeData.py ACS $f $count
    count=$((count + 1))
done