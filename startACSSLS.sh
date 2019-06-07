#!/bin/bash
count=1
for f in ./PFSP_instances/*.txt; do
	echo "ACS now"
    python solvePFSP_ACS_SLS.py --instance $f
    python writeData.py ACS_SLS $f $count
    count=$((count + 1))
done