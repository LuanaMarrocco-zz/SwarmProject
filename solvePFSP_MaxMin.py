import sys
from PFSP import PFSP
from ant import Ant

fileName = "PFSP_instances/DD_Ta051.txt"
alpha= 1.0
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
best_weighted_tardiness_ever = None
best_ant_ever = None

best_weighted_tardiness_tour = None
best_ant_tour = None

max_pheromone = None
min_pheromone = None
a_min_pheromone = 100

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
	p = PFSPobj.getProcessingTime()
	m = PFSPobj.getM()
	dueDates = PFSPobj.getDueDates()
	listHeuristic = [1.0] * N
	#Creation of the matric
	for i in range (N):
		listHeuristic[i] = 0.0
		heuristic.append(listHeuristic.copy())
		listHeuristic[i] = 1.0
	#Using the Widmer and Hertz distance
	"""for u in range(N):
		for v in range(N):
			d_uv = p[u][1*2+1] + p[v][-1]
			for k in range(2,m):
				add = (m-k)*abs(p[u][k*2+1]-p[u][(k-1)*2+1])
			d_uv += add
			heuristic[u][v] = 1/d_uv"""
	for i in range(N):
		for time in range(N):
			dist = dueDates[i] - time
			if (dist <= 0):
				dist = 0.01
			heuristic[i][time] = 1/dist

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
			probability[i][j] = pheromone[i][j]**alpha * heuristic[i][j]**beta

def createColony():
	global n_ants, PFSPobj, probability, seed, colony
	for i in range (n_ants):
		colony.append(Ant(PFSPobj, probability, seed))

def terminationCondition():
	global max_tours, tours, max_iterations, iterations
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
			checkPheromoneMaxMin(i,j)

def addPheromone(job, time, delta):
	global pheromone
	pheromone[job][time] += delta*100000
	checkPheromoneMaxMin(job,time)
	
#Deposit on the best tour of each iteration
def depositPheromoneMaxMin():
	global PFSPobj, best_weighted_tardiness_tour, best_ant_tour
	N = PFSPobj.getNumJobs()
	deltaf = (1.0/best_weighted_tardiness_tour)#TO DO Best tardiness ever ou best tardiness du tour?
	for j in range(N):
		addPheromone(best_ant_tour.getJob(j),j,deltaf)

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
	global PFSPobj, initial_pheromone,probability,colony, tours, iterations, best_weighted_tardiness_ever
	global best_ant_ever, max_pheromone, min_pheromone, a_min_pheromone, rho
	global best_ant_tour, best_weighted_tardiness_tour
	if(readArguments()):
		PFSPobj = PFSP(fileName)
		initializePheromone(initial_pheromone)
		initializeHeuristic()
		initializeProbabilities()
		calculateProbability()
		createColony()
		while(terminationCondition() == False):
			best_ant_tour = None
			best_weighted_tardiness_tour = None
			for i in range (n_ants):
				colony[i].search()
				print(colony[i].getWeightedTardiness())
				if(best_weighted_tardiness_ever == None or best_weighted_tardiness_ever > colony[i].getWeightedTardiness()):
					best_weighted_tardiness_ever = colony[i].getWeightedTardiness()
					best_ant_ever = colony[i]
					max_pheromone = 1/(rho*best_weighted_tardiness_ever)
					min_pheromone = max_pheromone/a_min_pheromone
				if(best_ant_tour == None or best_weighted_tardiness_tour > colony[i].getWeightedTardiness()):
					best_ant_tour = colony[i]
					best_weighted_tardiness_tour = colony[i].getWeightedTardiness()
				tours += 1
			evaporatePheromone()
			depositPheromoneMaxMin()
			calculateProbability()
			iterations += 1

		print("Voici la best ever: ",best_weighted_tardiness_ever)
		print(best_ant_ever.getSolution())




if __name__ == "__main__":
    main()

