fileName = "PFSP_instances/DD_Ta051.txt"
M = 0
N = 0
processingTime = [] #N lines, M colums
dueDates = []
weights = []

def readFile(filename):
	global M,N, processesTime, dueDates, weights
	f=open(filename, "r")
	lines = f.readlines()
	i = 0
	for line in lines:
		if(i == 0):
			N,M = list(map(int, line.split()))
			i = i+1
		elif(i <= N):
			processingTime.append(list(map(int, line.split())))
			i += 1
		else:
			content = line.split()
			if(content[0] != "Reldue"):
				_,date,_,weight = list(map(int, content))
				dueDates.append(date)
				weights.append(weight)

readFile(fileName)

