import sys
from PFSP import PFSP
from ant import Ant

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
heuristic = []
probability = []
colony = []


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
		listPheromone[i] = 0.0
		pheromone.append(listPheromone.copy())
		listPheromone[i] = initial_pheromone

def initializeHeuristic():
	global PFSPobj, heuristic
	N = PFSPobj.getNumJobs()
	listHeuristic = [1.0] * N
	for i in range (N):
		listHeuristic[i] = 0.0
		heuristic.append(listHeuristic.copy())
		listHeuristic[i] = 1.0

def initializeProbabilities():
	global PFSPobj, probability
	N = PFSPobj.getNumJobs()
	listProb = [0.0] * N
	for i in range(N):
		probability.append(listProb.copy())

def calculateProbability():
	global PFSPobj, probability, pheromone, heuristic, alpha, beta
	N = PFSPobj.getNumJobs()
	for i in range(0,N):
		for j in range(0,N):
			if(i == j):
				probability[i][j] = 0.0
			else:
				probability[i][j] = pheromone[i][j]**alpha * heuristic[i][j]**beta

def createColony():
	global n_ants, PFSPobj, probability, seed
	for i in range (n_ants):
		colony.append(Ant(PFSPobj, probability, seed))


def main() :
	global PFSPobj, initial_pheromone
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		initializePheromone(initial_pheromone)
		initializeHeuristic()
		initializeProbabilities()
		calculateProbability()
		createColony()


if __name__ == "__main__":
    main()

