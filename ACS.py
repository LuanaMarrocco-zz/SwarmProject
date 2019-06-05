import sys
from PFSP import PFSP
from ant_ACS import Ant

class ACS(object):
	def __init__(self, argv):
		self.fileNamePath = "PFSP_instances/"
		self.fileName = self.fileNamePath +"DD_Ta051.txt"
		self.resultFile = "resultsACS/" +self.fileName
		self.alpha=0.1
		self.beta=1.0
		self.rho=0.2
		self.n_ants=10
		self.max_iterations=10000
		self.seed = 0
		self.initial_pheromone = 1.0
		self.PFSPobj = None
		self.pheromone = []
		self.heuristic = []
		self.probability = []
		self.colony = []
		self.q0 = 0.5
		self.iterations = 0;
		self.best_weighted_tardiness = None
		self.best_ant = None

		self.readArguments(argv)
		self.PFSPobj = PFSP(self.fileName)
		self.initializePheromone()
		self.initializeHeuristic()
		self.initializeProbabilities()
		self.calculateProbability()
		self.createColony()
		while(self.terminationCondition() == False):
			for i in range (self.n_ants):
				self.colony[i].search()
				if(self.best_weighted_tardiness == None or self.best_weighted_tardiness > self.colony[i].getWeightedTardiness()):
					self.best_weighted_tardiness = self.colony[i].getWeightedTardiness()
					self.best_ant = self.colony[i]
					print("Voici la best ever: ",self.best_weighted_tardiness)
					print(self.best_ant.getSolution())
				self.calculateProbability()
			#evaporatePheromone()
			self.depositPheromone()
			self.calculateProbability()
			#print("Voici la best iteration: ",best_weighted_tardiness)
			self.iterations += 1
		print("Voici la best: ",self.best_weighted_tardiness)


	def readArguments(self,argv):
		i = 1
		retVal = True
		while(i < len(argv)):
			if(argv[i] == "--ants"):
				self.n_ants = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--alpha"):
				self.alpha = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--beta"):
				self.beta = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--rho"):
				self.rho = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--iterations"):
				self.max_iterations = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--tours"):
				self.max_tours = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--seed"):
				self.seed = int(argv[i+1])
				i += 1
			elif(sys.argv[i] == "--instance"):
				self.fileName = "PFSP_instances/"+sys.argv[i+1]
				self.resultFile = "results/" +self.fileName
				i += 1
			elif(sys.argv[i] == "--help"):
				self.printHelp()
				retVal = False
			else:
				print("Parameter ", argv[i], " not recognized")
				retVal = False
			i += 1
		return retVal

	def printHelp(self):
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
		helpString += str(self.initial_pheromone)
		print(helpString)

	def initializePheromone(self):
		pheromone = []
		N = self.PFSPobj.getNumJobs()
		listPheromone = [self.initial_pheromone] * N
		for i in range (N):
			self.pheromone.append(listPheromone.copy())

	def initializeHeuristic(self):
		N = self.PFSPobj.getNumJobs()
		p = self.PFSPobj.getProcessingTime()
		m = self.PFSPobj.getM()
		self.heuristic = []
		dueDates = self.PFSPobj.getDueDates()
		listHeuristic = [1.0] * N
		#Creation of the matric
		for i in range (N):
			self.heuristic.append(listHeuristic.copy())
		for i in range(N):
			for time in range(N):
				dist = dueDates[i]
				if (dist <= 0):
					dist = 1
				self.heuristic[i][time] = 1/dist

	def initializeProbabilities(self):
		N = self.PFSPobj.getNumJobs()
		listProb = [0.0] * N
		self.probability = []
		for i in range(N):
			self.probability.append(listProb.copy())

	def calculateProbability(self):
		N = self.PFSPobj.getNumJobs()
		for i in range(N):
			for j in range(N):
				self.probability[i][j] = self.pheromone[i][j]**self.alpha * self.heuristic[i][j]**self.beta

	def createColony(self):
		for i in range (self.n_ants):
			self.colony.append(Ant(self))

	def terminationCondition(self):
		res = False
		if (self.iterations >= self.max_iterations):
			res = True
		return res

	def evaporatePheromone(self):
		N = self.PFSPobj.getNumJobs()
		for i in range (N):
			for j in range (N):
				self.pheromone[i][j] = (1-self.rho)*self.pheromone[i][j]

	def addPheromone(self,job, time, delta):
		self.pheromone[job][time] = self.pheromone[job][time] + self.rho*delta *1000
		
	#Deposit on the global best tour
	def depositPheromone(self):
		N = self.PFSPobj.getNumJobs()
		deltaf = (1.0/self.best_weighted_tardiness)
		for j in range(N):
			self.addPheromone(self.best_ant.getJob(j),j,deltaf)

if __name__ == "__main__":
	ACSObj = ACS(sys.argv)