class Ant(object):

	def __init__(self, PFSP, probability, seed):
		self.size = PFSP.getNumJobs()
		self.PFSP = PFSP
		self.seed = seed
		self.probability = probability
		
	def search(self):
		print("I'm searching")

	def getTardiness(self):
		print("Best tardi")