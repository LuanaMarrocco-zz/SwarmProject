import sys
from PFSP import PFSP
from ant import Ant

fileName = "PFSP_instances/DD_Ta051.txt"
resultFile = "resultsMaxMin/" +fileName
alpha=0.01
beta=3.0
rho=0.4
n_ants=10
max_iterations=10000
seed = 0
initial_pheromone = 1.0
PFSPobj = None
pheromone = []
heuristic = []
probability = []
colony = []
countReInit = 0

iterations = 0;
best_weighted_tardiness_ever = None
best_ant_ever = None

best_weighted_tardiness_tour = None
best_ant_tour = None

max_pheromone = None
min_pheromone = None
a_min_pheromone = 1000

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
		--iterations: Maximum number of iterations to perform (interger). Default:10000.
		--seed: Number for the random seed generator.
		--instance: Path to the instance file
	ACO other parameters:
		initial pheromone: """
	helpString += str(initial_pheromone)
	print(helpString)

def readArguments():
	global n_ants,alpha,beta,rho, max_iterations, seed, fileName, resultFile
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
		elif(sys.argv[i] == "--seed"):
			seed = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--instance"):
			fileName = sys.argv[i+1]
			resultFile = "resultsMaxMin/" +fileName
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
	pheromone = []
	N = PFSPobj.getNumJobs()
	listPheromone = [initial_pheromone] * N
	for i in range (N):
		pheromone.append(listPheromone.copy())

def initializeHeuristic():
	global PFSPobj, heuristic
	N = PFSPobj.getNumJobs()
	p = PFSPobj.getProcessingTime()
	m = PFSPobj.getM()
	heuristic = []
	dueDates = PFSPobj.getDueDates()
	listHeuristic = [1.0] * N
	#Creation of the matric
	for i in range (N):
		listHeuristic[i] = 0.0
		heuristic.append(listHeuristic.copy())
		listHeuristic[i] = 1.0
	for i in range(N):
		for time in range(N):
			dist = dueDates[i]
			if (dist <= 0):
				dist = 1
			heuristic[i][time] = 1/dist

def initializeProbabilities():
	global PFSPobj, probability
	N = PFSPobj.getNumJobs()
	listProb = [0.0] * N
	probability = []
	for i in range(N):
		probability.append(listProb.copy())

def calculateProbability():
	global PFSPobj, probability, pheromone, heuristic, alpha, beta
	N = PFSPobj.getNumJobs()
	for i in range(N):
		for j in range(N):
			probability[i][j] = pheromone[i][j]**alpha * heuristic[i][j]**beta

def createColony():
	global n_ants, PFSPobj, probability, seed, colony
	for i in range (n_ants):
		colony.append(Ant(PFSPobj, probability, seed))

def terminationCondition():
	global max_iterations, iterations
	res = False
	if (iterations >= max_iterations):
		res = True
	return res

def evaporatePheromone():
	global PFSPobj,pheromone, rho
	N = PFSPobj.getNumJobs()
	for i in range (N):
		for j in range (N):
			pheromone[i][j] = (1-rho)*pheromone[i][j]
			checkPheromoneMaxMin(i,j)

def addPheromone(job, time, delta):
	global pheromone
	pheromone[job][time] += delta * 1000000
	checkPheromoneMaxMin(job,time)
	
#Deposit on the global best tour
def depositPheromoneMaxMin():
	global PFSPobj, best_weighted_tardiness_ever, best_ant_ever
	N = PFSPobj.getNumJobs()
	deltaf = (1.0/best_weighted_tardiness_ever)#TO DO Best tardiness ever ou best tardiness du tour?
	for j in range(N):
		addPheromone(best_ant_ever.getJob(j),j,deltaf)

def checkPheromoneMaxMin(job,time):
	global max_pheromone, pheromone, min_pheromone 
	if(max_pheromone != None):
		if(pheromone[job][time] > max_pheromone):
			pheromone[job][time] = max_pheromone
		elif(pheromone[job][time]< min_pheromone):
			pheromone[job][time] =  min_pheromone

def printPheromone():
	global pheromone
	print("Phéromone:")
	for elem in pheromone:
		print(elem)
	print()

def main() :
	global PFSPobj, initial_pheromone,probability,colony, iterations, best_weighted_tardiness_ever
	global best_ant_ever, max_pheromone, min_pheromone, a_min_pheromone, rho, pheromone, seed
	global best_ant_tour, best_weighted_tardiness_tour, countReInit
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		fichier = open(resultFile, "w")
		fichier.write("Total weighted tardiness\n")
		fichier.close()
		for run in range(10):
			seed=run
			initializePheromone(initial_pheromone)
			initializeHeuristic()
			initializeProbabilities()
			calculateProbability()
			createColony()
			best_ant_ever = None
			best_weighted_tardiness_ever = None 
			iterations = 0
			max_pheromone = None
			min_pheromone = None
			while(terminationCondition() == False):
				for i in range (n_ants):
					colony[i].search()
					if(best_weighted_tardiness_ever == None or best_weighted_tardiness_ever > colony[i].getWeightedTardiness()):
						best_weighted_tardiness_ever = colony[i].getWeightedTardiness()
						best_ant_ever = colony[i]
						max_pheromone = 1.0/(best_weighted_tardiness_ever*rho)*100000
						min_pheromone = max_pheromone/a_min_pheromone
						print("Best found: ", best_weighted_tardiness_ever)
						print(best_ant_ever.getSolution())
						countReInit = 0
				evaporatePheromone()
				depositPheromoneMaxMin()
				calculateProbability()
				iterations += 1
				countReInit += 1
				if(countReInit == 20):
					countReInit = 0
					initializePheromone(initial_pheromone)
					calculateProbability()
			fichier = open(resultFile, "a")
			fichier.write(str(best_weighted_tardiness_ever))
			fichier.write("\n")
			fichier.close()
	#printPheromone()



if __name__ == "__main__":
    main()

