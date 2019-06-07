#!/bin/bash
count=1
for f in ./PFSP_instances/*.txt; do
	echo "ACS SLS now"
    python solvePFSP_ACS_SLS.py --instance $f
    python writeData.py ACSSLS $f $count
    count=$((count + 1))
done