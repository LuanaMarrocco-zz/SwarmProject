# SwarmProject

To start MaxMin algo:
python solvePFSP_MaxMin.py --ants <int> --alpha <float> --beta <float> --rho <float> --tours <int> --iterations <int> --seed <int> --instance <path>

Example: python solvePFSP_MaxMin.py --tours 2000 --seed 123 --instance PFSP_instances/DD_Ta051.txt

To start ACS algo:
python solvePFSP_ACS.py --ants <int> --alpha <float> --beta <float> --rho <float> --tours <int> --iterations <int> --seed <int> --instance <path>

Example: python solvePFSP_ACS.py --tours 2000 --seed 123 --instance PFSP_instances/DD_Ta051.txt

To start ACS algo with local search:
python solvePFSP_ACS_SLS.py --ants <int> --alpha <float> --beta <float> --rho <float> --tours <int> --iterations <int> --seed <int> --instance <path>

Example: python solvePFSP_ACS_SLS.py --tours 2000 --seed 123 --instance PFSP_instances/DD_Ta051.txt
