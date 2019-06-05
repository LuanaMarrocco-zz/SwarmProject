import random
import numpy as np

class Ant(object):

	def __init__(self, PFSP, probability, seed, q0, pheromone, heuristic, alpha, beta, initialPheromone, rho):
		self.size = PFSP.getNumJobs()
		self.PFSP = PFSP
		self.seed = seed
		self.probability = probability
		self.solutionSequence = [-1] * self.size
		self.isAlreadySelected = [False] * self.size
		self.selectionProb = [0] * self.size
		self.completionTimeMatrix = []
		self.completionTime = None
		self.tardiness = [0] * self.size
		self.totalWeihtedTardiness = 0
		random.seed(self.seed)
		self.q0 = q0
		self.pheromone = pheromone
		self.heuristic = heuristic
		self.alpha = alpha
		self.beta = beta
		self.initialPheromone = initialPheromone
		self.rho = rho

	def search(self):
		self.clearSolution()
		self.solutionSequence[0] = int(random.random()*self.size)
		self.isAlreadySelected[self.solutionSequence[0]] = True
		
		#Selection of the next job
		for i in range(1,self.size):
			self.solutionSequence[i] = self.getNextJobACS(self.solutionSequence[i-1])
			self.isAlreadySelected[self.solutionSequence[i]] = True
		self.computeSolution()
		#print(self.solutionSequence)
	

		#Using the random proportional rule	
	def getNextJob(self, time):
		sumProb = 0.0
		for j in range (self.size):
			if(self.isAlreadySelected[j] == False):
				sumProb += self.probability[j][time]
			else:
				self.selectionProb[j] = 0.0
		
		for j in range(self.size):
			if(self.isAlreadySelected[j] == False):
				self.selectionProb[j] = self.probability[j][time]/sumProb 
		
		nextJob = np.random.choice(self.size, p=self.selectionProb)
		return nextJob

	#Using the state transition rule
	def getNextJobACS(self,previous):
		q = random.random()
		nextJob = 0
		if (q <= self.q0):
			maxVal = 0
			for i in range(self.size):
				if(self.isAlreadySelected[i] == False):
					val = self.pheromone[previous][i]*(self.heuristic[previous][i]**self.beta)
					if(val > maxVal):
						nextJob = i
						maxVal = val
		else:
			nextJob = self.getNextJob(previous)
		self.localUpdatePheromone(previous,nextJob)
		return nextJob

	def localUpdatePheromone(self, i, j):
		self.pheromone[i][j] = (1-self.rho)*self.pheromone[i][j] + self.rho*self.initialPheromone

	def computeSolution(self):
		self.computeCompletionTimeMatrix()
		self.computeTardinessList()
		self.computeTotelWeightedTardiness()

	def computeTardinessList(self):
		dueDates = self.PFSP.getDueDates()
		for i in range(self.size):
			valTardi = self.completionTime[i] - dueDates[self.solutionSequence[i]]
			tardi = max(0, valTardi)
			self.tardiness[i] = tardi

	def computeTotelWeightedTardiness(self):
		tot = 0
		weights = self.PFSP.getWeights()
		for i in range(self.size):
			tot = tot + self.tardiness[i]*weights[self.solutionSequence[i]]
		self.totalWeihtedTardiness = tot

	def computeCompletionTimeMatrix(self):
		M = self.PFSP.getM()
		processingTimes = self.PFSP.getProcessingTime()
		for i in range (M):
			completionTimePerMachine = []
			if (i==0):
				time = processingTimes[self.solutionSequence[0]][i*2+1]
				completionTimePerMachine.append(time)
				for j in range(1,self.size):
					time = time + processingTimes[self.solutionSequence[j]][i*2+1]
					completionTimePerMachine.append(time)
			else:
				for j in range(self.size):
					if(j==0):
						time = self.completionTimeMatrix[i-1][j]+processingTimes[self.solutionSequence[j]][i*2+1]
						completionTimePerMachine.append(time)
					else:
						maxVal = max(self.completionTimeMatrix[i-1][j],completionTimePerMachine[-1])
						time = maxVal + processingTimes[self.solutionSequence[j]][i*2+1]
						completionTimePerMachine.append(time)

			self.completionTimeMatrix.append(completionTimePerMachine)
		self.completionTime = self.completionTimeMatrix[-1]

	def getJob(self,i):
		return self.solutionSequence[i]

	def getWeightedTardiness(self):
		return self.totalWeihtedTardiness

	def getSolution(self):
		return self.solutionSequence

	def clearSolution(self):
		self.solutionSequence = [-1] * self.size
		self.isAlreadySelected = [False] * self.size
		self.selectionProb = [0] * self.size