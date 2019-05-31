fileName = "PFSP_instances/DD_Ta051.txt"
M = 0
N = 0
processesTime = []

def readFile(filename):
	global M,N, processesTime
	f=open(filename, "r")
	lines = f.readlines()
	i = 0
	for line in lines:
		if(i == 0):
			N,M = list(map(int, line.split()))
			i = i+1
		elif(i <= M):
			processesTime.append(list(map(int, line.split())))

			i += 1

readFile(fileName)
for elem in processesTime:
	print(elem)

