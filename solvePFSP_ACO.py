import sys
from PFSP import PFSP
from ant import Ant

fileName = "PFSP_instances/DD_Ta051.txt"
alpha=1.0
beta=1.0
rho=0.2
n_ants=10
max_iterations=10000
seed = 0
initial_pheromone = 1.0
PFSPobj = None
pheromone = []
heuristic = []
probability = []
colony = []

iterations = 0;
best_weighted_tardiness = None
best_ant = None

def printHelp():
	global initial_pheromone
	helpString = """	ACO Usage:
		./aco --ants <int> --alpha <float> --beta <float> --rho <float> --tours <int> --iterations <int> --seed <int> --instance <path>
		Example: ./aco --tours 2000 --seed 123 --instance eil151.tsp
	ACO flags:
		--ants: Number of ants to build every iteration. Default=10.
		--alpha: Alpha parameter (float). Default=1.
		--beta: Beta parameter (float). Default=1.
		--rho: Rho parameter (float). Defaut=0.2.
		--tours: Maximum number of tours to build (integer). Default=10000.
		--iterations: Maximum number of iterations to perform (interger). Default:0 (disabled).
		--seed: Number for the random seed generator.
		--instance: Path to the instance file
	ACO other parameters:
		initial pheromone: """
	helpString += str(initial_pheromone)
	print(helpString)

def readArguments():
	global n_ants,alpha,beta,rho, max_iterations, max_tours, seed, fileName
	i = 1
	retVal = True
	while(i < len(sys.argv)):
		if(sys.argv[i] == "--ants"):
			n_ants = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--alpha"):
			alpha = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--beta"):
			beta = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--rho"):
			rho = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--iterations"):
			max_iterations = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--tours"):
			max_tours = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--seed"):
			seed = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--instance"):
			fileName = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--help"):
			printHelp()
			retVal = False
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
		pheromone.append(listPheromone.copy())

def initializeHeuristic():
	global PFSPobj, heuristic
	N = PFSPobj.getNumJobs()
	listHeuristic = [1.0] * N
	for i in range (N):
		heuristic.append(listHeuristic.copy())
	for i in range (N):
		for j in range (N):
			heuristic[i][j] = PFSPobj.getDueDates()[i]

def initializeProbabilities():
	global PFSPobj, probability
	N = PFSPobj.getNumJobs()
	listProb = [0.0] * N
	for i in range(N):
		probability.append(listProb.copy())

def calculateProbability():
	global PFSPobj, probability, pheromone, heuristic, alpha, beta
	N = PFSPobj.getNumJobs()
	for i in range(N):
		for time in range(N):
			probability[i][time] = pheromone[i][time]**alpha * heuristic[i][time]**beta

def createColony():
	global n_ants, PFSPobj, probability, seed
	for i in range (n_ants):
		colony.append(Ant(PFSPobj, probability, seed))

def evaporatePheromone():
	global PFSPobj,pheromone, rho
	N = PFSPobj.getNumJobs()
	for i in range (N):
		for time in range (N):
			pheromone[i][time] = (1-rho)*pheromone[i][time]

def addPheromone(job1, time, delta):
	pheromone[job1][time] += delta*100000

def depositPheromone():
	global PFSPobj,n_ants,colony
	N = PFSPobj.getNumJobs()
	for i in range (n_ants):
		cost = colony[i].getWeightedTardiness()
		deltaf = 1.0/cost
		for j in range(N):
			addPheromone(colony[i].getJob(j),j,deltaf)

def main() :
	global PFSPobj, initial_pheromone,probability,colony, max_iterations, best_weighted_tardiness, best_ant
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		initializePheromone(initial_pheromone)
		initializeHeuristic()
		initializeProbabilities()
		calculateProbability()
		createColony()
		for it in range (max_iterations):
			for i in range (n_ants):
				colony[i].search()
				if(best_weighted_tardiness == None or best_weighted_tardiness > colony[i].getWeightedTardiness()):
					best_weighted_tardiness = colony[i].getWeightedTardiness()
					best_ant = colony[i]
			evaporatePheromone()
			depositPheromone()
			calculateProbability()
			print(it)

		print("Voici la best: ",best_weighted_tardiness)




if __name__ == "__main__":
    main()

