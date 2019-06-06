#!/bin/bash
pwd
for f in ./PFSP_instances/*.txt; do
    python solvePFSP_MaxMin.py --instance $f

done