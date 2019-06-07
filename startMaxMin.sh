#!/bin/bash
count=1
for f in ./PFSP_instances/*.txt; do
    #python solvePFSP_MaxMin.py --instance $f
    python writeData.py MaxMin $f $count
    count=$((count + 1))
done

count=1
for f in ./PFSP_instances/*.txt; do
	echo "ACS now"
    python solvePFSP_ACS.py --instance $f
    python writeData.py ACS $f $count
    count=$((count + 1))
done

