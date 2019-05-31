class PFSP(object):

	def __init__(self, fileName):
		self.fileName = fileName
		self.M = 0
		self.N = 0
		self.processingTime = [] #N lines, M colums
		self.dueDates = []
		self.weights = []
		self.readFile()

	def readFile(self):
		f=open(self.fileName, "r")
		lines = f.readlines()
		i = 0
		for line in lines:
			if(i == 0):
				self.N,self.M = list(map(int, line.split()))
				i = i+1
			elif(i <= self.N):
				self.processingTime.append(list(map(int, line.split())))
				i += 1
			else:
				content = line.split()
				if(content[0] != "Reldue"):
					_,date,_,weight = list(map(int, content))
					self.dueDates.append(date)
					self.weights.append(weight)
	
	def getNumJobs(self):
		return self.N

