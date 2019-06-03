import random

class Ant(object):

	def __init__(self, PFSP, probability, seed):
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
		
	def search(self):
		self.clearSolution()
		self.solutionSequence[0] = int(random.random()*self.size)
		self.isAlreadySelected[self.solutionSequence[0]] = True
		
		#Selection of the next job
		for i in range(1,self.size):
			self.solutionSequence[i] = self.getNextJob(self.solutionSequence[i-1])
			self.isAlreadySelected[self.solutionSequence[i]] = True
		self.computeSolution()
	

	#TO DO	
	def getNextJob(self, previous):
		sumProb = 0.0
		for j in range (self.size):
			if(self.isAlreadySelected[j] == False and j != previous):
				sumProb += self.probability[previous][j]
				self.selectionProb[j] = sumProb
			else:
				self.selectionProb[j] = 0.0
		
		#TO DO: Pour le moment je prend betement le prochain dans l'ordre
		if(sumProb <= 0):
			print("coucou je suis dans getNextJob sumProb <= 0")
			nextJob = (previous+1)%self.size
			while(self.isAlreadySelected[nextJob] == True):
				nextJob = (nextJob + 1) % self.size
		else:
			choice = random.random()*sumProb
			nextJob = 0
			while(choice > self.selectionProb[nextJob]):
				nextJob += 1
		return nextJob

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

	def clearSolution(self):
		self.solutionSequence = [-1] * self.size
		self.isAlreadySelected = [False] * self.size
		self.selectionProb = [0] * self.size