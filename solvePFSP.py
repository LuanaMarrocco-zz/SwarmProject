import sys
from PFSP import PFSP

fileName = "PFSP_instances/DD_Ta051.txt"
alpha=1.0
beta=1.0
rho=0.2
n_ants=10
max_iterations=0
max_tours=10000
seed = 0
initial_pheromone = 1.0
PFSPobj = None
pheromone = []


def readArguments():
	global n_ants,alpha,beta,rho, max_iterations, max_tours, seed, fileName
	i = 1
	retVal = True
	while(i < len(sys.argv)):
		if(sys.argv[i] == "--ants"):
			n_ants = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--alpha"):
			alpha = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--beta"):
			beta = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--rho"):
			rho = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--iterations"):
			max_iterations = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--tours"):
			max_tours = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--seed"):
			seed = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--instance"):
			fileName = sys.argv[i+1]
			i += 1
		else:
			print("Parameter ", sys.argv[i], " not recognized")
			retVal = False
		i += 1
	return retVal

def initializePheromone(initial_pheromone):
	global PFSPobj, pheromone
	N = PFSPobj.getNumJobs()
	listPheromone = [initial_pheromone] * N
	for i in range (N):
		listPheromone[i] = 0
		pheromone.append(listPheromone.copy())
		listPheromone[i] = initial_pheromone






def main() :
	global PFSPobj, initial_pheromone
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		initializePheromone(initial_pheromone)

if __name__ == "__main__":
    main()

