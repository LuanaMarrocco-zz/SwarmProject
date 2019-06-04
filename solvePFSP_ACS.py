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

tours = 0;
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
	for i in range(N):
		for j in range(N):
			if(i == j):
				probability[i][j] = 0.0
			else:
				probability[i][j] = pheromone[i][j]**alpha * heuristic[i][j]**beta

def createColony():
	global n_ants, PFSPobj, probability, seed
	for i in range (n_ants):
		colony.append(Ant(PFSPobj, probability, seed))

def terminationCondition():
	res = False
	if(max_tours != 0 and tours > max_tours):
		res = True
	if(max_iterations !=0 and iterations >= max_iterations):
		res = True
	return res

def evaporatePheromone():
	global PFSPobj,pheromone, rho
	N = PFSPobj.getNumJobs()
	for i in range (N):
		for j in range (N):
			pheromone[i][j] = (1-rho)*pheromone[i][j]

def addPheromone(job1, job2, delta):
	pheromone[job1][job2] += delta

def depositPheromone():
	global PFSPobj,n_ants,colony
	N = PFSPobj.getNumJobs()
	for i in range (n_ants):
		deltaf = 1.0/colony[i].getWeightedTardiness()
		for j in range(1,N):
			addPheromone(colony[i].getJob(j-1),colony[i].getJob(j),deltaf)
		addPheromone(colony[i].getJob(-1), colony[i].getJob(0), deltaf)

def main() :
	global PFSPobj, initial_pheromone,probability,colony, tours, iterations, best_weighted_tardiness, best_ant
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		initializePheromone(initial_pheromone)
		initializeHeuristic()
		initializeProbabilities()
		calculateProbability()
		createColony()
		while(terminationCondition() == False):
			for i in range (n_ants):
				colony[i].search()
				if(best_weighted_tardiness == None or best_weighted_tardiness > colony[i].getWeightedTardiness()):
					best_weighted_tardiness = colony[i].getWeightedTardiness()
					best_ant = colony[i]
				tours += 1
			evaporatePheromone()
			depositPheromone()
			calculateProbability()

		iterations += 1
		print("Voici la best: ",best_weighted_tardiness)




if __name__ == "__main__":
    main()

